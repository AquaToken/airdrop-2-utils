import logging
import operator
from decimal import ROUND_DOWN, Decimal
from functools import reduce
from multiprocessing import Pool
from typing import Iterable, Optional

from sqlalchemy.orm import Session
from stellar_sdk import Asset, Keypair

from airdrop2_utils.constants.airdrop import (
    AIRDROP_CAP,
    AIRDROP_CAP_EXCEPTIONS,
    AIRDROP_VALUE,
    AQUA_REQUIREMENTS,
    LOCK_START_TIMESTAMP,
    MAX_LOCK_BOOST,
    MAX_LOCK_TERM,
    XLM_REQUIREMENTS,
)
from airdrop2_utils.constants.assets import AQUA, XLM, YXLM
from airdrop2_utils.constants.stellar import XLM_TO_STROOP
from airdrop2_utils.data import AirdropAccount, LiquidityPoolData, LiquidityPoolParticipant, Lock
from airdrop2_utils.stellar_core_db.models import ClaimableBalance
from airdrop2_utils.stellar_core_db.queries import (
    get_airdrop_candidates,
    get_all_claimable_balances,
    get_asset_liquidity_pool,
    get_trustline_for_liquidity_pools,
)
from airdrop2_utils.stellar_core_db.types_cast import (
    pack_trust_line_asset,
    unpack_claimable_balance,
    unpack_liquidity_pool_data,
    unpack_trust_line_balance,
)


logger = logging.getLogger(__name__)


def load_airdrop_candidates(*, session: Session) -> Iterable[AirdropAccount]:
    query = get_airdrop_candidates()

    for account, yxlm_trust_line, aqua_trust_line in session.execute(query):
        native_balance = account.balance / XLM_TO_STROOP
        aqua_balance = unpack_trust_line_balance(aqua_trust_line.ledgerentry) / XLM_TO_STROOP
        if yxlm_trust_line:
            yxlm_balance = unpack_trust_line_balance(yxlm_trust_line.ledgerentry) / XLM_TO_STROOP
        else:
            yxlm_balance = Decimal(0)

        if native_balance + yxlm_balance < XLM_REQUIREMENTS or aqua_balance < AQUA_REQUIREMENTS:
            continue

        yield AirdropAccount(
            account_id=account.accountid,
            native_balance=account.balance,
            aqua_balance=aqua_balance,
            yxlm_balance=yxlm_balance,
        )


def load_liquidity_pool_data(asset: Asset, *, session: Session) -> Iterable[LiquidityPoolData]:
    query = get_asset_liquidity_pool(asset)

    trust_line_asset_xdr = pack_trust_line_asset(asset)
    for liquidity_pool, in session.execute(query):
        reserve_a, reserve_b, total_shares = unpack_liquidity_pool_data(liquidity_pool.ledgerentry)

        if liquidity_pool.asseta == trust_line_asset_xdr:
            reserve = reserve_a
        else:
            reserve = reserve_b

        yield LiquidityPoolData(
            pool_asset=liquidity_pool.poolasset,
            reserved_asset=asset,
            asset_reserve=reserve / XLM_TO_STROOP,
            total_shares=total_shares / XLM_TO_STROOP,
        )


def load_liquidity_pool_participants(asset: Asset, *, session: Session) -> Iterable[LiquidityPoolParticipant]:
    liquidity_pool_data_dict = {
        pool['pool_asset']: pool for pool in load_liquidity_pool_data(asset, session=session)
    }

    query = get_trustline_for_liquidity_pools(liquidity_pool_data_dict.keys())

    for trust_line, in session.execute(query):
        pool_data = liquidity_pool_data_dict[trust_line.asset]
        if pool_data['total_shares'] == 0:
            continue

        pool_shares = unpack_trust_line_balance(trust_line.ledgerentry) / XLM_TO_STROOP
        reserved_balance = (
            (pool_shares * pool_data['asset_reserve'] / pool_data['total_shares'])
            .quantize(1 / XLM_TO_STROOP, rounding=ROUND_DOWN)
        )

        yield LiquidityPoolParticipant(
            account_id=trust_line.accountid,
            reserved_asset=asset,
            reserved_balance=reserved_balance,
        )


def reduce_liquidity_pool_participants(
    participants: Iterable[LiquidityPoolParticipant],
) -> Iterable[LiquidityPoolParticipant]:
    accumulator = {}
    for participant in participants:
        accumulated_participant = accumulator.get(participant['account_id'])
        if not accumulated_participant:
            accumulated_participant = LiquidityPoolParticipant(
                account_id=participant['account_id'],
                reserved_asset=participant['reserved_asset'],
                reserved_balance=Decimal(0),
            )
            accumulator[participant['account_id']] = accumulated_participant

        accumulated_participant['reserved_balance'] += participant['reserved_balance']

    yield from accumulator.values()


def parse_lock(claimable_balance: ClaimableBalance) -> Optional[Lock]:
    claimable_balance_entry, sponsor = unpack_claimable_balance(claimable_balance.ledgerentry)
    if claimable_balance_entry.asset != AQUA.to_xdr_object():
        return

    if len(claimable_balance_entry.claimants) != 1:
        return

    claimant = claimable_balance_entry.claimants[0]
    if sponsor != claimant.v0.destination.account_id:
        return

    predicate = claimant.v0.predicate
    if not predicate.not_predicate or not predicate.not_predicate.abs_before:
        return

    unlock_at = predicate.not_predicate.abs_before.int64
    if unlock_at < LOCK_START_TIMESTAMP:
        return

    account_keypair = Keypair.from_raw_ed25519_public_key(claimant.v0.destination.account_id.ed25519.uint256)

    return Lock(
        account_id=account_keypair.public_key,
        amount=claimable_balance_entry.amount.int64,
        term=min(unlock_at - LOCK_START_TIMESTAMP, MAX_LOCK_TERM),
    )


def load_locks(*, session: Session) -> Iterable[Lock]:
    query = get_all_claimable_balances()
    claimable_balances = (balance for balance, in session.execute(query))

    with Pool() as pool:
        for index, lock in enumerate(pool.imap_unordered(parse_lock, claimable_balances)):
            if index % 1000 == 0:
                logger.info(f'Parsed claimable balance #{index}.')

            if not lock:
                continue

            yield lock


def reduce_locks(locks: Iterable[Lock]) -> Iterable[Lock]:
    accumulator = {}
    for lock in locks:
        accumulated_lock = accumulator.get(lock['account_id'])
        if not accumulated_lock:
            accumulated_lock = {
                'numerator': Decimal(0),
                'amount': Decimal(0),
            }
            accumulator[lock['account_id']] = accumulated_lock

        accumulated_lock['numerator'] += lock['term'] * lock['amount']
        accumulated_lock['amount'] += lock['amount']

    for account_id, accumulated_lock in accumulator.items():
        yield Lock(
            account_id=account_id,
            amount=accumulated_lock['amount'],
            term=int(accumulated_lock['numerator'] / accumulated_lock['amount']),
        )


def load_airdrop_accounts(*, session: Session, aqua_price: Decimal) -> Iterable[AirdropAccount]:
    native_pool_data = reduce_liquidity_pool_participants(load_liquidity_pool_participants(XLM, session=session))
    native_pool_dict = {
        pool['account_id']: pool for pool in native_pool_data
    }
    yxlm_pool_data = reduce_liquidity_pool_participants(load_liquidity_pool_participants(YXLM, session=session))
    yxlm_pool_dict = {
        pool['account_id']: pool for pool in yxlm_pool_data
    }
    aqua_pool_data = reduce_liquidity_pool_participants(load_liquidity_pool_participants(AQUA, session=session))
    aqua_pool_dict = {
        pool['account_id']: pool for pool in aqua_pool_data
    }

    logger.info('Pool data loaded.')

    locks_data = reduce_locks(load_locks(session=session))
    locks_dict = {
        lock['account_id']: lock for lock in locks_data
    }

    logger.info('Locks data loaded.')

    for index, candidate in enumerate(load_airdrop_candidates(session=session)):
        if index % 1000 == 0:
            logger.info(f'Process airdrop candidate #{index}.')

        native_pool_participant = native_pool_dict.get(candidate['account_id'])
        yxlm_pool_participant = yxlm_pool_dict.get(candidate['account_id'])
        aqua_pool_participant = aqua_pool_dict.get(candidate['account_id'])

        candidate['native_pool_balance'] = (
            native_pool_participant['reserved_balance'] if native_pool_participant else Decimal(0)
        )
        candidate['yxlm_pool_balance'] = (
            yxlm_pool_participant['reserved_balance'] if yxlm_pool_participant else Decimal(0)
        )
        candidate['aqua_pool_balance'] = (
            aqua_pool_participant['reserved_balance'] if aqua_pool_participant else Decimal(0)
        )

        lock = locks_dict.get(candidate['account_id'])
        if lock:
            candidate['aqua_lock_balance'] = lock['amount']
            candidate['aqua_lock_term'] = lock['term']
        else:
            candidate['aqua_lock_balance'] = Decimal(0)
            candidate['aqua_lock_term'] = 0

        xlm_balance = (
            candidate['native_balance'] + candidate['yxlm_balance']
            + candidate['native_pool_balance'] + candidate['yxlm_pool_balance']
        )
        aqua_balance = candidate['aqua_balance'] + candidate['aqua_pool_balance']

        unlocked_shares = xlm_balance + aqua_price * aqua_balance
        locked_shares = aqua_price * candidate['aqua_lock_balance']

        user_value_lock_multiplier = min(locked_shares, unlocked_shares) / unlocked_shares
        user_time_lock_multiplier = Decimal(min(MAX_LOCK_TERM, candidate['aqua_lock_term']) / MAX_LOCK_TERM)

        user_total_lock_multiplier = user_value_lock_multiplier * user_time_lock_multiplier
        user_boost = MAX_LOCK_BOOST * user_total_lock_multiplier

        candidate['airdrop_shares'] = (unlocked_shares + locked_shares) * (1 + user_boost)

        yield candidate


def set_airdrop_rewards(airdrop_accounts: Iterable[AirdropAccount]) -> Iterable[AirdropAccount]:
    accounts_to_distribute = list(airdrop_accounts)
    aqua_to_distribute = AIRDROP_VALUE

    while True:
        total_airdrop_shares = reduce(operator.add,
                                      map(operator.itemgetter('airdrop_shares'), accounts_to_distribute),
                                      Decimal(0))
        share_price = aqua_to_distribute / total_airdrop_shares
        logger.info(f'Current share price based on {len(accounts_to_distribute)} accounts is {share_price}.')

        index = 0
        account_cut_off = False
        while index < len(accounts_to_distribute):
            account = accounts_to_distribute[index]
            airdrop_reward = account['airdrop_shares'] * share_price
            if airdrop_reward <= AIRDROP_CAP or account['account_id'] in AIRDROP_CAP_EXCEPTIONS:
                account['airdrop_reward'] = airdrop_reward
                index += 1
                continue

            logger.info(f'{account["account_id"]} cut off with rewards {airdrop_reward}.')

            account['airdrop_reward'] = AIRDROP_CAP
            aqua_to_distribute -= AIRDROP_CAP
            accounts_to_distribute.pop(index)
            account_cut_off = True

            yield account

        if not account_cut_off:
            break

    yield from accounts_to_distribute
