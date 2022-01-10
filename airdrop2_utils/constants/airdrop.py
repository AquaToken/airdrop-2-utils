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
    'GATHSLHLMK3OFQKRSMSCOODEFABR2GWMVW2LUESZZPL6ZHMVCVP5JBXU',
    'GBE27W2DJZS4AFFR2HVZBK4KHD4TQQ4ITB2AQTYA5L57K6ZTRWPJUDH6',
    'GBP3BTNFQKP65QZTJQRKCUSZKUO66KFTH53SM5LR2SAMFRBJWKNKJAOK',
    'GCOEPUFA4VGWIEEYCSTLOJX2OTUYZ42M6C7HNX4NANIRUNKOFCBXCBHY',
    'GBHMB55GUN23HBWH4YGRPEZWHNL523JTUBS6KSCQ5OPTN4KHYRPJVE6S',
    'GAGCX4RX6OAZMPNRGDMHLQ7OMHXZM7I3CZO2ISXCJ3OMNDPE5Q7ENCDA',
    'GCAXOLGVBICF3CY5ESBLCBBKACSVBJ55XTK4NO3FDZ5UIK3BRABCCWZC',
    'GA7XXJ3PGGSOX2A5YAAFDFIZDMODHGWVL7RQTKIUKWCZAQYLIH7SNMFZ',
    'GBFP2QMU46T4TWUMTF6GX7EZQEY3F3IM2O6E6IRIRNDFXQZO26S5HNIG',
]
