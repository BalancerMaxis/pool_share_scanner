import os
from datetime import datetime

from pool_share_scanner.constants import BALANCER_SUBGRAPH_MAINNET, BALANCER_GAUGE_SUBGRAPH_MAINNET
from pool_share_scanner.data_merger import process_balancer_pool_user_bpts
from pool_share_scanner.utils import write_results_to_csv, get_block_by_ts


def main():
    # Ensure the output directory exists
    output_dir = "balancer"
    os.makedirs(output_dir, exist_ok=True)
    # Pool and Gauge pairing
    pool_gauge_pairs = {
        "0x05ff47afada98a98982113758878f9a8b9fdda0a000000000000000000000645": "0xc859bf9d7b8c557bbd229565124c2c09269f3aef"
    }
    # Generate filename with block number and timestamp
    timestamp = datetime.now()
    block = get_block_by_ts(timestamp, 'mainnet')
    file_timestamp = int(timestamp.timestamp())
    filename = f"{output_dir}/balancer_data_{block}_{file_timestamp}.csv"

    # Process data
    merged_data = process_balancer_pool_user_bpts(pool_gauge_pairs, block, BALANCER_SUBGRAPH_MAINNET, BALANCER_GAUGE_SUBGRAPH_MAINNET)

    # Write results to CSV
    write_results_to_csv(merged_data, filename)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
