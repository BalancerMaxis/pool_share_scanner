from utils import fetch_graphql_data


def fetch_pool_data(pool_id, block, endpoint):
    query = """
    query GetUserPoolBalances($poolId: ID!, $block: Int) {
        pool(id: $poolId, block: {number: $block}) {
            shares(where: {balance_gt: "0"}, orderBy: balance, orderDirection: desc) {
                userAddress {
                    id
                }
                balance
            }
        }
    }
    """
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
    query = """
    query FetchGaugeShares($gaugeAddress: String!, $block: Int) {
      gaugeShares(
        block: {number: $block}
        where: {gauge_contains_nocase: $gaugeAddress, balance_gt: "1"}
        orderBy: balance
        orderDirection: desc
        first: 1000
      ) {
        balance
        id
        user {
          id
        }
      }
    }
    """
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
