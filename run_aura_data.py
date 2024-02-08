import os
from datetime import datetime
from pool_share_scanner.constants import AURA_SUBGRAPH_BY_CHAIN
from pool_share_scanner.data_fetcher import fetch_aura_pool_shares
from pool_share_scanner.utils import write_results_to_csv, get_block_by_ts


def main():
    # Ensure the output directory exists
    output_dir = "aura"
    os.makedirs(output_dir, exist_ok=True)

    # --- MAINNET ---
    # Pool and Gauge pairing
    pool_gauge_pairs_mainnet = {
        "182": "0xc859bf9d7b8c557bbd229565124c2c09269f3aef",  # rETH-weETH
        "189": "0xa8b309a75f0d64ed632d45a003c68a30e59a1d8b",  # ezETH-WETH
        "191": "0x0bcdb6d9b27bd62d3de605393902c7d1a2c71aab",  # rsETH-ETHx
    }

    # Generate filename with block number and timestamp
    timestamp = datetime.now()
    block = get_block_by_ts(timestamp, 'mainnet')  # Assuming get_block_by_ts accepts an int timestamp
    file_timestamp = int(timestamp.timestamp())
    filename = f"{output_dir}/aura_data_mainnet_{block}_{file_timestamp}.csv"

    # Initialize a list to hold all fetched and merged results
    merged_results = []

    # Fetch data for each pool in pool_gauge_pairs and merge
    for pool_id, gauge_id in pool_gauge_pairs_mainnet.items():
        pool_results = fetch_aura_pool_shares(pool_id, block, AURA_SUBGRAPH_BY_CHAIN['mainnet'])
        # Enrich fetched data with the corresponding gauge_id
        for result in pool_results:
            result['gauge_id'] = gauge_id  # Update gauge_id in each result
        merged_results.extend(pool_results)  # Merge into the final list

    # Write results to CSV
    write_results_to_csv(merged_results, filename)
    print(f"Data saved to {filename}")

    # --- ZKEVM ---
    pool_gauge_pairs_zkevm = {
        "5": "0x047301b311741ce6c007ffef7f182ec93ab07968",  # rsETH-ETHx
    }

    filename_zkevm = f"{output_dir}/aura_data_zkevm_{block}_{file_timestamp}.csv"
    block_zkevm = get_block_by_ts(timestamp, 'zkevm')
    merged_results_zkevm = []

    # Fetch data for each pool in pool_gauge_pairs and merge
    for pool_id, gauge_id in pool_gauge_pairs_zkevm.items():
        pool_results = fetch_aura_pool_shares(pool_id, block_zkevm, AURA_SUBGRAPH_BY_CHAIN['zkevm'])
        # Enrich fetched data with the corresponding gauge_id
        for result in pool_results:
            result['gauge_id'] = gauge_id  # Update gauge_id in each result
        merged_results.extend(pool_results)  # Merge into the final list

    # Write results to CSV
    write_results_to_csv(merged_results_zkevm, filename_zkevm)
    print(f"Data saved to {filename_zkevm}")


if __name__ == "__main__":
    main()
