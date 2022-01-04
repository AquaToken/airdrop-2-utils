import argparse
import csv
import logging
from datetime import datetime

from airdrop2_utils.horizon import get_aqua_price
from airdrop2_utils.snapshot import set_airdrop_rewards, load_airdrop_accounts
from airdrop2_utils.stellar_core_db.session import make_session

logger = logging.getLogger(__name__)


def make_snapshot(db_url, output_file, *, tuples_only):
    now = datetime.utcnow()
    aqua_price = get_aqua_price(now)

    logger.info('AQUA price loaded.')

    with make_session(db_url) as session:
        snapshot = list(set_airdrop_rewards(load_airdrop_accounts(session=session, aqua_price=aqua_price)))

    logger.info(f'Save snapshot to {output_file}.')

    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f)

        if not tuples_only:
            csv_writer.writerow([
                'Account id',
                'Native balance',
                'yXLM balance',
                'AQUA balance',
                'Native AMM balance',
                'yXLM AMM balance',
                'AQUA AMM balance',
                'Locked AQUA balance',
                'Lock terms',
                'Airdrop shares',
                'Airdrop rewards',
            ])

        for airdrop_account in snapshot:
            csv_writer.writerow([
                airdrop_account['account_id'],
                airdrop_account['native_balance'],
                airdrop_account['yxlm_balance'],
                airdrop_account['aqua_balance'],
                airdrop_account['native_pool_balance'],
                airdrop_account['yxlm_pool_balance'],
                airdrop_account['aqua_pool_balance'],
                airdrop_account['aqua_lock_balance'],
                airdrop_account['aqua_lock_term'],
                airdrop_account['airdrop_shares'],
                airdrop_account['airdrop_reward'],
            ])


if __name__ == '__main__':
    # TODO: Add descriptions
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=False, default='user=stellar dbname=stellar')
    parser.add_argument('--output', required=False, default='snapshot.csv')
    parser.add_argument('--tuples-only', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    make_snapshot(args.db, args.output, tuples_only=args.tuples_only)
