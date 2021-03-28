# Ethereum ETL Table Definition CLI

Ethereum ETL Table Definition CLI allows you to generate table definitions for Ethereum ETL. 

Read this article for more details: [How to get any Ethereum smart contract into BigQuery (in 8 mins)](https://towardsdatascience.com/how-to-get-any-ethereum-smart-contract-into-bigquery-in-8-mins-bab5db1fdeee).

## Quickstart

Install the cli:

```bash
pip install ethereum-etl-table-definition-cli
```

Generate table definitions (`example_uniswap_abi.json` can be downloaded from [here](https://github.com/blockchain-etl/ethereum-etl-table-definition-cli/blob/main/example_uniswap_abi.json)):

```bash
tabledefinition generate \
    --abi-file example_uniswap_abi.json \
    --dataset-name uniswap \
    --contract-name Uni \
    --contract-address 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
```

Output will be in the `output` directory.

---

For the latest version, check out the repo and call 
```bash
pip install -e . 
```