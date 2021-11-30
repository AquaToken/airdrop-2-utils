import argparse

import psycopg2
from stellar_sdk import Asset


AQUA_CODE = 'AQUA'
AQUA_ISSUER = 'GBNZILSTVQZ4R7IKQDGHYGY2QXL5QOFJYQMXPKWRRM5PAV7Y4M67AQUA'

YXLM_CODE = 'yXLM'
YXLM_ISSUER = 'GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55'

XLM_REQUIREMENT = 500 * (10 ** 7)  # 500 xlm in stroops


TRUSTLINES_SQL = '''SELECT * FROM trustlines where asset = %s'''
ACCOUNTS_SQL = f'''
    SELECT ACC.accountid, ACC.balance, AQUA.ledgerentry, YXLM.ledgerentry
    FROM accounts ACC
        RIGHT JOIN ({TRUSTLINES_SQL}) AQUA ON ACC.accountid = AQUA.accountid
        LEFT JOIN ({TRUSTLINES_SQL}) YXLM ON ACC.accountid = YXLM.accountid
    WHERE ACC.balance > %s OR YXLM.accountid IS NOT NULL
    LIMIT 5
'''


def load_airdrop_candidate(db_url):
    aqua_asset_entry = Asset(AQUA_CODE, AQUA_ISSUER).to_trust_line_asset_xdr_object().to_xdr()
    yxlm_asset_entry = Asset(YXLM_CODE, YXLM_ISSUER).to_trust_line_asset_xdr_object().to_xdr()

    with psycopg2.connect(db_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(ACCOUNTS_SQL, (aqua_asset_entry, yxlm_asset_entry, XLM_REQUIREMENT))
            data = cursor.fetchone()
            print(data)


if __name__ == '__main__':
    # TODO: Add descriptions
    parser = argparse.ArgumentParser()
    parser.add_argument('db', default='postgres://dbname=stellar user=stellar')
    args = parser.parse_args()

    load_airdrop_candidate('postgres://user=stellar dbname=stellar2')
