import argparse
import contextlib
import csv
import logging
from decimal import Decimal

import psycopg2
from stellar_sdk import Asset
from stellar_sdk.xdr import LedgerEntry


logger = logging.getLogger(__name__)


XLM_TO_STROOP = Decimal(10 ** 7)


AQUA_CODE = 'AQUA'
AQUA_ISSUER = 'GBNZILSTVQZ4R7IKQDGHYGY2QXL5QOFJYQMXPKWRRM5PAV7Y4M67AQUA'

YXLM_CODE = 'yXLM'
YXLM_ISSUER = 'GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55'

XLM_REQUIREMENTS = 500
AQUA_REQUIREMENTS = 1
STROOPS_REQUIREMENTS = XLM_REQUIREMENTS * XLM_TO_STROOP  # 500 xlm in stroops


TRUSTLINES_SQL = '''SELECT * FROM trustlines where asset = %s'''
ACCOUNTS_SQL = f'''
    SELECT ACC.accountid, ACC.balance, AQUA.ledgerentry, YXLM.ledgerentry
    FROM accounts ACC
        RIGHT JOIN ({TRUSTLINES_SQL}) AQUA ON ACC.accountid = AQUA.accountid
        LEFT JOIN ({TRUSTLINES_SQL}) YXLM ON ACC.accountid = YXLM.accountid
    WHERE ACC.balance > %s OR YXLM.accountid IS NOT NULL
'''


def load_db_records(db_url):
    aqua_asset_entry = Asset(AQUA_CODE, AQUA_ISSUER).to_trust_line_asset_xdr_object().to_xdr()
    yxlm_asset_entry = Asset(YXLM_CODE, YXLM_ISSUER).to_trust_line_asset_xdr_object().to_xdr()

    logger.debug('Connecting to database: %s', db_url)
    with psycopg2.connect(db_url) as connection:
        with connection.cursor(name='aqua_airdrop2_snapshot_cursor', scrollable=True) as cursor:
            logger.info('Loading accounts data')

            cursor.itersize = 100
            cursor.execute(ACCOUNTS_SQL, (aqua_asset_entry, yxlm_asset_entry, STROOPS_REQUIREMENTS))

            yield from cursor


def parse_airdrop_candidate(db_record):
    logger.debug('Parsing record: %s', db_record)

    account_id, native_balance, aqua_ledger_entry, yxlm_ledger_entry = db_record

    native_balance = native_balance / XLM_TO_STROOP
    aqua_balance = LedgerEntry.from_xdr(aqua_ledger_entry).data.trust_line.balance.int64 / XLM_TO_STROOP
    if yxlm_ledger_entry:
        yxlm_balance = LedgerEntry.from_xdr(yxlm_ledger_entry).data.trust_line.balance.int64 / XLM_TO_STROOP
    else:
        yxlm_balance = 0

    return account_id, native_balance, aqua_balance, yxlm_balance


@contextlib.contextmanager
def get_csv_writer(output_file, *, tuples_only):
    with open(output_file, 'w') as f:
        snapshot_writer = csv.writer(f)

        if not tuples_only:
            snapshot_writer.writerow(['Account id', 'Native balance', 'yXLM balance',
                                      'Total XLM balance', 'AQUA balance'])

        yield snapshot_writer


def load_airdrop_accounts(db_url, output_file, *, tuples_only):
    with get_csv_writer(output_file, tuples_only=tuples_only) as csv_writer:
        for db_record in load_db_records(db_url):
            account_id, native_balance, aqua_balance, yxlm_balance = parse_airdrop_candidate(db_record)
            logger.info('Record parsed: %s', account_id)

            if aqua_balance < AQUA_REQUIREMENTS or native_balance + yxlm_balance < XLM_REQUIREMENTS:
                logger.info('Requirements missed. Skipping %s', account_id)
                continue

            csv_writer.writerow([account_id, str(native_balance), str(yxlm_balance),
                                 str(native_balance + yxlm_balance), str(aqua_balance)])


if __name__ == '__main__':
    # TODO: Add descriptions
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=False, default='user=stellar dbname=stellar')
    parser.add_argument('--output', required=False, default='snapshot.csv')
    parser.add_argument('--tuples-only', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    load_airdrop_accounts(args.db, args.output, tuples_only=args.tuples_only)
