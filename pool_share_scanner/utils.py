import requests
import csv

from gql import Client
from gql import gql
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

from pool_share_scanner.constants import BLOCKS_BY_CHAIN, BLOCKS_QUERY


def fetch_graphql_data(endpoint, query, variables):
    response = requests.post(endpoint, json={'query': query, 'variables': variables})
    data = response.json()
    if 'errors' in data:
        print(f"Error: {data['errors']}")
        return None
    return data


def write_results_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['block', 'poolId', 'gaugeId', 'userAddress', 'balancer_bpt'])
        for result in results:
            writer.writerow(
                [result['block'], result['pool_id'], result['gauge_id'], result['user_address_id'], result['balance']])


def get_block_by_ts(timestamp: datetime, chain: str) -> int:
    """
    Returns block number for a given timestamp (datetime object).
    """
    # Convert the datetime object to a Unix timestamp (seconds since the epoch)
    timestamp_unix = int(timestamp.timestamp())

    current_timestamp = int(datetime.now().timestamp())
    if timestamp_unix > current_timestamp:
        timestamp_unix = current_timestamp - 2000

    transport = RequestsHTTPTransport(
        url=BLOCKS_BY_CHAIN[chain],
        retries=2,
    )

    query = gql(
        BLOCKS_QUERY.format(
            ts_gt=timestamp_unix - 200,
            ts_lt=timestamp_unix + 200,
        )
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    result = client.execute(query)

    # Assuming the query ensures only one block is returned, sorting is unnecessary
    return int(result["blocks"][0]["number"])
