from pool_share_scanner.constants import BALANCER_POOL_SHARES_QUERY, BALANCER_GAUGES_SHARES_QUERY, AURA_SHARES_QUERY
from utils import fetch_graphql_data
from typing import Dict
from typing import List

def fetch_pool_data(pool_id, block, endpoint):
    query = BALANCER_POOL_SHARES_QUERY
    variables = {"poolId": pool_id, "block": block}
    data = fetch_graphql_data(endpoint, query, variables)
    results = []
    if data and 'data' in data and 'pool' in data['data'] and data['data']['pool']:
        for share in data['data']['pool']['shares']:
            results.append({
                'block': block,
                'pool_id': pool_id,
                'gauge_id': '-',  # Default to '-' when gauge data is not merged yet
                'user_address_id': share['userAddress']['id'],
                'balance': share['balance']
            })
    return results


def fetch_gauge_data(gauge_id, block, endpoint):
    query = BALANCER_GAUGES_SHARES_QUERY
    variables = {
        "gaugeAddress": gauge_id,
        "block": block
    }
    data = fetch_graphql_data(endpoint, query, variables)
    results = []
    if 'data' in data and 'gaugeShares' in data['data']:
        for share in data['data']['gaugeShares']:
            results.append({
                'user_address_id': share['user']['id'],
                'balance': share['balance'],
                'gauge_id': gauge_id  # Include gauge ID for merging
            })
    return results


def fetch_aura_pool_shares(pool_id, block, endpoint):
    # Prepare the GraphQL query and variables
    variables = {"poolId": pool_id, "block": block}
    data = fetch_graphql_data(endpoint, AURA_SHARES_QUERY, variables)
    results = []

    # Parse the data if the query was successful
    if data and 'data' in data and 'leaderboard' in data['data'] and data['data']['leaderboard']['accounts']:
        for account in data['data']['leaderboard']['accounts']:
            results.append({
                'block': block,
                'pool_id': pool_id,
                'gauge_id': '-',  # Default placeholder for gauge_id
                'user_address_id': account['account']['id'],
                'balance': account['staked']
            })
    return results


def fetch_aura_shares_by_user(pool_id: str, block: int,  endpoint: str) -> Dict[str, Dict]:
    # Prepare the GraphQL query and variables
    variables = {"poolId": pool_id, "block": block}
    data = fetch_graphql_data(endpoint, AURA_SHARES_QUERY, variables)
    balance_by_user = {}

    # Parse the data if the query was successful
    if data and 'data' in data and 'leaderboard' in data['data'] and data['data']['leaderboard']['accounts']:
        for account in data['data']['leaderboard']['accounts']:
            userAddress = account['account']['id']
            if userAddress in balance_by_user.keys():
                raise Exception("User shows up twice in a list of users and amounts?")
            else:
                balance_by_user[userAddress] = account['staked']
    return balance_by_user


def fetch_pool_data_by_user(pool_id: str, block: int,  endpoint: str) -> Dict[str, Dict]:
    query = BALANCER_POOL_SHARES_QUERY
    variables = {"poolId": pool_id, "block": block}
    data = fetch_graphql_data(endpoint, query, variables)
    results = []
    if data and 'data' in data and 'pool' in data['data'] and data['data']['pool']:
        for share in data['data']['pool']['shares']:
            results.append({
                'block': block,
                'pool_id': pool_id,
                'gauge_id': '-',  # Default to '-' when gauge data is not merged yet
                'user_address_id': share['userAddress']['id'],
                'balance': share['balance']
            })
    return results
