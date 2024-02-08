BALANCER_SUBGRAPH_MAINNET = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
BALANCER_GAUGE_SUBGRAPH_MAINNET = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-gauges"
AURA_SUBGRAPH_MAINNET = "https://graph.aura.finance/subgraphs/name/aura/aura-mainnet-v2-1"

BALANCER_GAUGE_SUBGRAPH_BY_CHAIN = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-gauges",
    "zkevm": ""
}

BALANCER_SUBGRAPH_BY_CHAIN = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2",
    "zkevm": ''
}


BLOCKS_BY_CHAIN = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/blocklytics/ethereum-blocks",
    "arbitrum": "https://api.thegraph.com/subgraphs/name/ianlapham/arbitrum-one-blocks",
    "polygon": "https://api.thegraph.com/subgraphs/name/ianlapham/polygon-blocks",
    "base": "https://api.studio.thegraph.com/query/48427/bleu-base-blocks/version/latest",
    "gnosis": "https://api.thegraph.com/subgraphs/name/rebase-agency/gnosis-chain-blocks",
    "avalanche": "https://api.thegraph.com/subgraphs/name/iliaazhel/avalanche-blocks",
    "zkevm": "https://api.studio.thegraph.com/query/48427/bleu-polygon-zkevm-blocks/version/latest",
}

BLOCKS_QUERY = """
query {{
    blocks(where:{{timestamp_gt: {ts_gt}, timestamp_lt: {ts_lt} }}) {{
    number
    timestamp
    }}
}}
"""

# --- BALANCER QUERIES ---
BALANCER_POOL_SHARES_QUERY = """
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

BALANCER_GAUGES_SHARES_QUERY = """
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

# --- AURA QUERIES ---
AURA_SHARES_QUERY = """
    query PoolLeaderboard($poolId: ID!, $block: Int) {
      leaderboard: pool(id: $poolId, block: {number: $block}) {
        accounts(
          first: 1000
          where: {staked_gt: 1}
          orderBy: staked
          orderDirection: desc
        ) {
          staked
          pool {
            id
          }
          account {
            id
          }
        }
        totalStaked
      }
    }
    """
