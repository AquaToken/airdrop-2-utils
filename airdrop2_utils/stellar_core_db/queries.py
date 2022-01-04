from typing import Iterable

from sqlalchemy import or_, select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import Select
from stellar_sdk import Asset

from airdrop2_utils.constants.assets import AQUA, YXLM
from airdrop2_utils.stellar_core_db.models import Account, LiquidityPool, TrustLine, ClaimableBalance
from airdrop2_utils.stellar_core_db.types_cast import pack_trust_line_asset


def get_asset_trust_line(asset: Asset) -> Select:
    return select(TrustLine).filter(TrustLine.asset == pack_trust_line_asset(asset))


def get_airdrop_candidates() -> Select:
    aqua_trust_line_query = aliased(
        TrustLine,
        get_asset_trust_line(AQUA).subquery(name='aqua_trust_line'),
    )
    yxlm_trust_line_query = aliased(
        TrustLine,
        get_asset_trust_line(YXLM).subquery(name='yxlm_trust_line'),
    )

    return (
        select(Account, yxlm_trust_line_query, aqua_trust_line_query)
        .join(aqua_trust_line_query, aqua_trust_line_query.accountid == Account.accountid)
        .join(yxlm_trust_line_query, yxlm_trust_line_query.accountid == Account.accountid, isouter=True)
    )


def get_asset_liquidity_pool(asset: Asset) -> Select:
    trust_line_xdr = pack_trust_line_asset(asset)

    return select(LiquidityPool).where(
        or_(
            LiquidityPool.asseta == trust_line_xdr,
            LiquidityPool.assetb == trust_line_xdr,
        ),
    )


def get_trustline_for_liquidity_pools(pool_asset_list: Iterable[str]) -> Select:
    return select(TrustLine).where(TrustLine.asset.in_(pool_asset_list))


def get_all_claimable_balances() -> Select:
    return select(ClaimableBalance)
