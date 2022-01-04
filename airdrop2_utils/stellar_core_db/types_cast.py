from typing import Union

from stellar_sdk import Asset, LiquidityPoolAsset
from stellar_sdk.xdr import AssetType, Hash, LedgerEntry, PoolID, TrustLineAsset, ClaimableBalanceEntry, PublicKey


def pack_trust_line_asset(asset: Union[Asset, LiquidityPoolAsset]) -> str:
    if isinstance(asset, Asset):
        return asset.to_trust_line_asset_xdr_object().to_xdr()

    if isinstance(asset, LiquidityPoolAsset):
        return TrustLineAsset(
            type=AssetType.ASSET_TYPE_POOL_SHARE,
            liquidity_pool_id=PoolID(Hash(bytes.fromhex(asset.liquidity_pool_id))),
        ).to_xdr()


def unpack_ledger_entry(xdr: str) -> LedgerEntry:
    return LedgerEntry.from_xdr(xdr)


def unpack_trust_line_balance(xdr: str) -> int:
    ledger_entry = unpack_ledger_entry(xdr)
    return ledger_entry.data.trust_line.balance.int64


def unpack_liquidity_pool_data(xdr: str) -> (int, int, int):
    ledger_entry = unpack_ledger_entry(xdr)
    constant_product = ledger_entry.data.liquidity_pool.body.constant_product
    return (
        constant_product.reserve_a.int64,
        constant_product.reserve_b.int64,
        constant_product.total_pool_shares.int64,
    )


def unpack_claimable_balance(xdr: str) -> (ClaimableBalanceEntry, PublicKey):
    ledger_entry = unpack_ledger_entry(xdr)
    sponsor = ledger_entry.ext.v1.sponsoring_id.sponsorship_descriptor.account_id
    return ledger_entry.data.claimable_balance, sponsor
