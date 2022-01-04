from datetime import datetime, timezone
from decimal import Decimal


XLM_REQUIREMENTS = Decimal(500)
AQUA_REQUIREMENTS = Decimal(1)


LOCK_START = datetime(year=2022, month=1, day=15, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
LOCK_START_TIMESTAMP = int(LOCK_START.timestamp())
LOCK_END = datetime(year=2025, month=1, day=15, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
LOCK_END_TIMESTAMP = int(LOCK_END.timestamp())
MAX_LOCK_TERM = LOCK_END_TIMESTAMP - LOCK_START_TIMESTAMP
MAX_LOCK_BOOST = 3


AIRDROP_VALUE = Decimal(15 * 10 ** 9)
AIRDROP_CAP = Decimal(10 * 10 ** 6)
AIRDROP_CAP_EXCEPTIONS = [
    'GCWEER57MBVRXA4I426VL3PSWWM72SSZ3AZ5TGBDSWJMTDFVCABWNZIF',
    'GCXDR4QZ4OTVX6433DPTXELCSEWQ4E5BIPVRRJMUR6M3NT4JCVIDALZO',
    'GAZANXSPY2N3MANBJYLATYGMXDLHZMO57KDST6AN5MOKXEP3OBUFPV66',
]
