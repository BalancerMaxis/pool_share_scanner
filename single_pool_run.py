import os
from datetime import datetime, timedelta
from pool_share_scanner.constants import BALANCER_GAUGE_SUBGRAPH_BY_CHAIN, BALANCER_SUBGRAPH_BY_CHAIN
from pool_share_scanner.data_merger import process_balancer_pool_user_bpts
from pool_share_scanner.utils import write_results_to_csv, get_block_by_ts

def main(gen_file=False, pool=None, gauge=None, block=None, chain=None):

    if not pool:
        pool = os.getenv("POOL_ID")
    if not block:
        block = os.getenv("RUN_BLOCK")
    if not gauge:
        gauge = os.getenv("GAUGE_ADDRESS")
    if not chain:
        chain = "mainnet"
    total_balances = {}
    process_balancer_pool_user_bpts({pool: gauge}), block, BALANCER_SUBGRAPH_BY_CHAIN[chain], BALANCER_GAUGE_SUBGRAPH_BY_CHAIN[chain])
    if gen_file:
        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

