from decimal import Decimal
from typing import TypedDict

from stellar_sdk import Asset


class AirdropAccount(TypedDict, total=False):
    account_id: str

    native_balance: Decimal
    yxlm_balance: Decimal
    aqua_balance: Decimal

    native_pool_balance: Decimal
    yxlm_pool_balance: Decimal
    aqua_pool_balance: Decimal

    aqua_lock_balance: Decimal
    aqua_lock_term: int

    airdrop_shares: Decimal
    airdrop_reward: Decimal


class LiquidityPoolData(TypedDict):
    pool_asset: str
    reserved_asset: Asset

    asset_reserve: Decimal
    total_shares: Decimal


class LiquidityPoolParticipant(TypedDict):
    account_id: str
    reserved_asset: Asset
    reserved_balance: Decimal


class Lock(TypedDict):
    account_id: str
    amount: Decimal
    term: int
