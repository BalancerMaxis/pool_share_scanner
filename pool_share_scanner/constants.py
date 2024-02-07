BALANCER_SUBGRAPH_MAINNET = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
BALANCER_GAUGE_SUBGRAPH_MAINNET = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-gauges"
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
