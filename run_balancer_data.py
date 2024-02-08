import os
from datetime import datetime, timedelta

from pool_share_scanner.constants import BALANCER_GAUGE_SUBGRAPH_BY_CHAIN, BALANCER_SUBGRAPH_BY_CHAIN
from pool_share_scanner.data_merger import process_balancer_pool_user_bpts
from pool_share_scanner.utils import write_results_to_csv, get_block_by_ts


def main():
    # Ensure the output directory exists
    output_dir = "balancer"
    os.makedirs(output_dir, exist_ok=True)

    # --- MAINNET ---
    # Pool and Gauge pairing
    pool_gauge_pairs_mainnet = {
        "0x7761b6e0daa04e70637d81f1da7d186c205c2ade00000000000000000000065d": "0x0bcdb6d9b27bd62d3de605393902c7d1a2c71aab",  # rsETH-ETHx
        "0x05ff47afada98a98982113758878f9a8b9fdda0a000000000000000000000645": "0xc859bf9d7b8c557bbd229565124c2c09269f3aef",  # rETH-weETH
        "0xdedb11a6a23263469567c2881a9b9f8629ee0041000000000000000000000669": "-",                                           # svETH-wstETH
        "0x596192bb6e41802428ac943d2f1476c1af25cc0e000000000000000000000659": "0xa8b309a75f0d64ed632d45a003c68a30e59a1d8b"   # ezETH-WETH
    }

    # Generate filename with block number and timestamp
    timestamp = datetime.now() - timedelta(minutes=1)
    block = get_block_by_ts(timestamp, 'mainnet')
    file_timestamp = int(timestamp.timestamp())
    filename = f"{output_dir}/balancer_data_mainnet_{block}_{file_timestamp}.csv"

    # Process data (TODO: refactor to fetch endpoints from dict)
    merged_data = process_balancer_pool_user_bpts(pool_gauge_pairs_mainnet, block,
                                                  BALANCER_SUBGRAPH_BY_CHAIN['mainnet'],
                                                  BALANCER_GAUGE_SUBGRAPH_BY_CHAIN['mainnet'])

    # Write results to CSV
    write_results_to_csv(merged_data, filename)
    print(f"Data saved to {filename}")

    # --- ZKEVM ---
    pool_gauge_pairs_zkevm = {
        "0xffc865fcb34e754fad4b0144139b9c28c81c3eff00000000000000000000005f": '0x047301b311741ce6c007ffef7f182ec93ab07968'  # rsETH-WETH
    }
    block_zkevm = get_block_by_ts(timestamp, 'zkevm')
    filename_zkevm = f"{output_dir}/balancer_data_zkevm_{block_zkevm}_{file_timestamp}.csv"
    merged_data_zkevm = process_balancer_pool_user_bpts(pool_gauge_pairs_zkevm, block_zkevm,
                                                        BALANCER_SUBGRAPH_BY_CHAIN['zkevm'],
                                                        BALANCER_GAUGE_SUBGRAPH_BY_CHAIN['zkevm'])

    write_results_to_csv(merged_data_zkevm, filename_zkevm)
    print(f"Data saved to {filename_zkevm}")


if __name__ == "__main__":
    main()
