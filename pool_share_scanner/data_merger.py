from pool_share_scanner.data_fetcher import fetch_pool_data, fetch_gauge_data


def process_balancer_pool_user_bpts(pool_gauge_pairs, block, pool_endpoint, gauge_endpoint):
    pool_results = []
    gauge_results = {}
    for pool_id, gauge_id in pool_gauge_pairs.items():
        # Fetch pool data
        pool_data = fetch_pool_data(pool_id, block, pool_endpoint)
        pool_results.extend(pool_data)

        # Fetch gauge data if gauge_id is provided and not already fetched
        if gauge_id and gauge_id not in gauge_results:
            gauge_data = fetch_gauge_data(gauge_id, block, gauge_endpoint)
            gauge_results[gauge_id] = gauge_data

    # Correctly merge pool and gauge data using the refined function
    merged_data = merge_pool_and_gauge_data(pool_results, gauge_results, pool_gauge_pairs, block)
    return merged_data


def merge_pool_and_gauge_data(pool_data, gauge_data, pool_gauge_pairs, block):
    # Reverse lookup for gauge to pool
    gauge_to_pool = {v: k for k, v in pool_gauge_pairs.items()}

    # Create a lookup for gauge data
    gauge_lookup = {share['user_address_id']: share for gauge_id, shares in gauge_data.items() for share in shares}

    merged_data = []
    for pool_item in pool_data:
        user_id = pool_item['user_address_id']
        # Exclude entries where userAddress matches gaugeId
        if user_id in gauge_to_pool:  # Check against gauge_to_pool for direct match
            continue
        if user_id in gauge_lookup:
            # Merge gauge data into pool data if user exists in both
            gauge_item = gauge_lookup.pop(user_id)
            pool_item['balance'] = str(float(pool_item['balance']) + float(gauge_item['balance']))  # Sum balances
            pool_item['gauge_id'] = gauge_item['gauge_id']
        else:
            # If user is not in gauge data, append with "-" as gauge_id
            pool_item['gauge_id'] = '-'
        merged_data.append(pool_item)

    # Add remaining gauge entries not matched with pool data
    for user_id, gauge_item in gauge_lookup.items():
        gauge_id = gauge_item['gauge_id']
        # Exclude entries where userAddress is the gauge itself
        if user_id == gauge_id:  # Corrected the check here
            continue
        pool_id = gauge_to_pool.get(gauge_id, '-')  # Use pool_id corresponding to gauge_id, if available
        merged_data.append({
            'block': block,
            'pool_id': pool_id,  # Always populated, using mapping from gauge to pool
            'gauge_id': gauge_id,
            'user_address_id': user_id,
            'balance': gauge_item['balance']
        })

    return merged_data