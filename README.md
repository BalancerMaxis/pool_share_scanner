# Important Disclaimer
This is a MVP project to showcase how to fetch subgraph data to evaluate BPT shares. **Use this repository if you want to integrate it into your pipeline: https://github.com/BalancerMaxis/ecosystem_balances_example** 
# Pool Share Scanner

The Pool Share Scanner is a tool designed for fetching and aggregating user stake information from both Balancer and
Aura DeFi platforms. It queries subgraphs for specified pools and gauges, merges the data, and outputs the results into
CSV files for easy analysis and reporting.

## Features

- Fetch stake data from specified Balancer pools and gauges.
- Fetch stake data from specified Aura pools.
- Merge fetched data into a cohesive structure.
- Output the merged data into CSV files, separated by source (Balancer or Aura).

## Output Data

### BALANCER
- Examples of non-staked BPT shares (no gauge ID)

| block    | poolId                                                             | gaugeId | userAddress                                | balancer_bpt            |
|----------|--------------------------------------------------------------------|---------|--------------------------------------------|-------------------------|
| 19181967 | 0x7761b6e0daa04e70637d81f1da7d186c205c2ade00000000000000000000065d | -       | 0xa23f54e0bb57a6114d831c080823f5fe2616cf98 | 1016.006977848476827924 |
| 19181967 | 0x7761b6e0daa04e70637d81f1da7d186c205c2ade00000000000000000000065d | -       | 0x5a14bd3f2bf84c3690d653f1d40cfb7a8a9b3c26 | 401.040230750106664973  |
| 19181967 | 0x7761b6e0daa04e70637d81f1da7d186c205c2ade00000000000000000000065d | -       | 0x1adcf07389b1f6605c44a7683c50a5243829a92c | 39.9606093855569484     |

### AURA
- Example of user shares in an Aura gauge

| block    | poolId | gaugeId | userAddress                                | balancer_bpt          |
|----------|--------|---------|--------------------------------------------|-----------------------|
| 19181989 | 182    | -       | 0x41bc7d0687e6cea57fa26da78379dfdc5627c56d | 396272844435693001697 |
| 19181989 | 182    | -       | 0x29c7b44e0584624c1e877d3ee0856520e2851ba6 | 247518661716231060183 |
| 19181989 | 182    | -       | 0x324b9d99da9a586e7510f1ca7f48f1d6885e6eb1 | 228428749087637312738 |

### How to read the output data

#### BALANCER

- For Balancer pool data, poolId corresponds to the pool BPTs (Balancer pool tokens) are deposited. If there is not
  gauge entry, it means that the depositor did not stake
- A gauge address entry next to the poolId indicates, that user address has funds deposited in the gauge
- Note: The Aura depositor address is not yet removed -> TODO

#### AURA

- Aura has convex-style poolIDs. Check constants for reference which poolID corresponds to the balancer pool
- Aura shares are currently exported as raw amounts
- The total of all aura shares should correspond to the bpt entry int he balancer export with the aura address as
  userAddress

## How to Use

### Prerequisites

- Python 3.6 or higher.
- Required Python packages: `requests`, `pandas` (for DataFrame support, if utilized).

### Setup

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt` from the root directory of the
   project.

### Running the Tool

Navigate to the project directory and execute one of the runner scripts depending on the data you wish to fetch and
merge:

- For Balancer data:
  ```bash
  python run_balancer_data.py

- For Aura data:
  ```bash
  python run_aura_data.py

Each script will automatically fetch data for the configured pool-gauge pairs, process the data, and save the output to
a CSV file in a directory named after the data source (balancer or aura).
Data is fetched for the block corresponding to the execution timestamp. This can be overwritten if desired.

### Configuration

- **Pool and Gauge Pairings**: Edit the pool_gauge_pairs dictionary in the respective runner script to specify which
  pools and gauges to query.
- **Constants:** Modify constants.py to update GraphQL endpoint URLs as needed.

### TODOs / Limitations

- Only fetches data for mainnet
- Not all gauges active yet
- no label of Aura depositor address