## PyAirbyte Data Pipelines 101

In this first practical exercise you will build a minimal yet complete pipeline that streams Stripe data into a local DuckDB cache from inside a Google Colab notebook. The same code can later be pasted into a plain Python file and scheduled from GitHub Actions or any orchestrator.

### Set up the environment

Create or open a new Colab notebook and install PyAirbyte:

```bash
# Prepare env and install PyAirbyte
!apt-get update && apt-get install -qq python3.11-venv
%pip install airbyte
```

Import the package to verify the installation:

```python
import airbyte as ab
```

### Explore the connector catalogue

PyAirbyte exposes a helper that lists every source and destination available in the Airbyte registry:

```python
available_sources = ab.get_available_connectors()

for source in available_sources:
    print(source)
```

Running `len(available_sources)` shows more than **550** connectors—each one ready to be called from pure Python.

### Choose a source: Stripe

For the walkthrough we will pull data from Stripe, using its public test key so everyone can follow along. If you prefer another API, swap the connector name and credentials and the remainder of the steps remain identical.

> **Note**  
> When you run PyAirbyte inside Colab you must install the connector package yourself; in a regular script PyAirbyte can install missing packages automatically.

Install the Stripe connector:

```bash
%pip install airbyte-source-stripe
```

If the last line reads `Successfully installed airbyte-source-stripe‑…` you are ready to continue.

### Initialise the source and authenticate

Go to <a href="https://docs.stripe.com/api" target="_blank">Stripe API Documentation Page</a> and copy the API key. 
It is a test-sample API Key Stripe provide to run tests.

```python
source = ab.get_source(
    "source-stripe",
    install_if_missing=False  # set to True in non‑Colab environments
)

source.set_config(
    {
        "account_id": "",
        "client_secret": "API_KEY",
    }
)

source.check()  # should print “Connection check succeeded”
```

### Inspect streams

A source may expose dozens of endpoints (Stripe offers `events`, `charges`, `balance_transactions`, and many more). List them:

```python
source.get_available_streams()
```

### Select and read data

Choose one or several streams:

```python
source.select_streams("balance_transactions")  # or a list / all streams
read_result = source.read()
```

PyAirbyte now streams records into an in‑process DuckDB file while keeping track of incremental state.

The command prints progress logs; when it finishes you’ll see an output resembling the screenshot below.

![image](https://hackmd.io/_uploads/HysQO7TRkx.png)

View the data:

```python
balance_df = read_result["balance_transactions"].to_pandas()
balance_df.head()
```

![image](https://hackmd.io/_uploads/ryPkUy2Ckl.png)


You installed PyAirbyte, explored the connector catalogue, authenticated to a real API, selected a stream, and materialised the results in local DuckDB with fewer than 25 lines of code. Behind the scenes PyAirbyte stored state so that subsequent runs retrieve only new or updated records.

The notebook pipeline works, but it is still ephemeral. In the next section we will persist the data to MotherDuck, manage secrets safely, and prepare the code for scheduled production runs.


