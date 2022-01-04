from datetime import datetime, timezone, timedelta
from decimal import Decimal

import requests

from airdrop2_utils.constants.assets import AQUA_CODE, AQUA_ISSUER
from airdrop2_utils.constants.stellar import HORIZON_URL


def get_aqua_price(now: datetime):
    today = now.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    last_week = today - timedelta(days=7)

    resp = requests.get(f'{HORIZON_URL.rstrip("/")}/trade_aggregations/', params={
        'base_asset_type': 'native',
        'counter_asset_type': 'credit_alphanum4',
        'counter_asset_code': AQUA_CODE,
        'counter_asset_issuer': AQUA_ISSUER,
        'start_time': int(last_week.timestamp()) * 1000,  # Convert to milliseconds
        'end_time': int(today.timestamp()) * 1000,  # Convert to milliseconds
        'resolution': 86400000,  # 1 day
    })

    xlm_volume = 0
    aqua_volume = 0
    for record in resp.json()['_embedded']['records']:
        xlm_volume += Decimal(record['base_volume'])
        aqua_volume += Decimal(record['counter_volume'])

    return Decimal(round(xlm_volume / aqua_volume, 7))
