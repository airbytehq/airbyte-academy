## Durable Pipelines & Vector Destinations

The notebook pipeline you built in the previous section is useful for exploration but remains ephemeral. In this module you will persist data to MotherDuck, keep credentials out of source control, and see how the very same records can be routed into a vector database for semantic search or Retrieval‑Augmented Generation (RAG).

### 1  Using secrets

PyAirbyte can auto-import secrets from the following sources:
* Environment variables.
* Variables defined in a local .env ("Dotenv") file.
* Google Colab secrets.
* Google Secret Manager.
* Manual entry via getpass.

> [!Note]
> You can also create your custom Secret Manager if you need to retrieve secret from AWS or Azure as at the moment PyAirbyte doesnt support them. Check instructions <a href="https://airbytehq.github.io/PyAirbyte/airbyte/secrets.html#CustomSecretManager" target="_blank">here</a>

In our case let's use the Google Colab secrets.
Go to Motherduck and create a new account if you don't have it. It's free. After, create a new database called `pyairbyte` and get the Token from Motherduck Settings panel to allow us control Motherduck using code. You can check instructions <a href="https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/" target="_blank">here</a>.

After you have the Motherduck Token, create a Google Colab Secret called `MOTHERDUCK_APIKEY`
![image](https://hackmd.io/_uploads/S1b92y3RJe.png)


### 2  Persist data with MotherDuck

A local DuckDB file disappears when the Colab kernel is reset. Switching the cache to **MotherDuck** makes the dataset durable and shareable.

```python
from airbyte.caches import MotherDuckCache

cache = MotherDuckCache(
    database="pyairbyte",
    schema="lms",
    api_key=ab.get_secret("MOTHERDUCK_APIKEY"),  # pulled from Colab secrets
)

result = source.read(cache=cache)
```

* `MotherDuckCache` replaces the default in‑memory cache.
* `ab.get_secret()` looks in Colab secrets, dotenv, environment variables, or Google Secret Manager—no explicit store selection required.
* State tables are created automatically so incremental syncs continue to work.

After the run completes you will see four tables in MotherDuck, including `_airbyte_state` and your data stream (`balance_transactions`).



```python
from airbyte.caches import MotherDuckCache
 
cache = MotherDuckCache(
    database="pyairbyte",
    schema="lms",
    api_key=ab.get_secret("MOTHERDUCK_APIKEY"),
)
result = source.read(cache=cache)
```

1. import `MotherDuckCache` now instead of using the ephemeral DuckDbCache, PyAirbyte's default, we're going to use one option will keep the data after we finish running the pipeline or reset it.
2. `ab.get_secret("MOTHERDUCK_APIKEY")` PyAirbyte is going to try to find a secret in all 4 places describe before. You don't need to declare where they're.
3. `source.read(cache=cache)` we're overriding the default cache to use the one we created and send data to Motherduck.


Run the code above and after check Motherduck.
![image](https://hackmd.io/_uploads/S1c20y2Rkl.png)
We have 4 tables:
* `_airbyte_destination_state` and `_airbyte_state` are require to make incremental syncs possible.
* `_airbyte_streams` stores metadata about the pipeline, what stream, names and the schema for each of them.
* Finally the data table, in our case `balance_transactions`.

Click in Preview Data to see the results:
![image](https://hackmd.io/_uploads/HJSOOX6R1e.png)

> [!Tip]
> If you run the code above again it will retrieve only 1 or 0 new records because it has the state save in Motherduck. So every new run will only retrieve new records. This is true when the stream support incremental reading if not will execute a full refresh (reading all data again). This is a limitation in the API service side doesn't allow to filter data.
> 

### 3  Extend reach with custom connectors

The Airbyte registry covers hundreds of APIs, but sooner or later you will need an endpoint that is not yet available. PyAirbyte can run a **manifest‑only declarative connector**—no build or container registry required. In this example we're going to use a manifest-only connector to read data from the Rick and Morty API.
We're not going to teach you how to build a custom connector in this course, but you can read the <a href="https://docs.airbyte.com/connector-development/" target="_blank">documentation</a> to learn more.

```python
SOURCE_MANIFEST_TEXT = """
version: 0.85.0


type: DeclarativeSource

check:
  type: CheckStream
  stream_names:
    - characters

definitions:
  streams:
    characters:
      type: DeclarativeStream
      name: characters
      primary_key:
        - id
      retriever:
        type: SimpleRetriever
        requester:
          $ref: '#/definitions/base_requester'
          path: character/
          http_method: GET
          error_handler:
            type: CompositeErrorHandler
            error_handlers:
              - type: DefaultErrorHandler
                response_filters:
                  - type: HttpResponseFilter
                    action: SUCCESS
                    error_message_contains: There is nothing here
        record_selector:
          type: RecordSelector
          extractor:
            type: DpathExtractor
            field_path:
              - results
        paginator:
          type: DefaultPaginator
          page_token_option:
            type: RequestOption
            inject_into: request_parameter
            field_name: page
          pagination_strategy:
            type: PageIncrement
            start_from_page: 1
      schema_loader:
        type: InlineSchemaLoader
        schema:
          $ref: '#/schemas/characters'
  base_requester:
    type: HttpRequester
    url_base: https://rickandmortyapi.com/api

streams:
  - $ref: '#/definitions/streams/characters'

spec:
  type: Spec
  connection_specification:
    type: object
    $schema: http://json-schema.org/draft-07/schema#
    required: []
    properties: {}
    additionalProperties: true

metadata:
  autoImportSchema:
    characters: true

schemas:
  characters:
    type: object
    $schema: http://json-schema.org/schema#
    properties:
      type:
        type:
          - string
          - 'null'
      created:
        type:
          - string
          - 'null'
      episode:
        type:
          - array
          - 'null'
        items:
          type:
            - string
            - 'null'
      gender:
        type:
          - string
          - 'null'
      id:
        type: number
      image:
        type:
          - string
          - 'null'
      location:
        type:
          - object
          - 'null'
        properties:
          name:
            type:
              - string
              - 'null'
          url:
            type:
              - string
              - 'null'
      name:
        type:
          - string
          - 'null'
      origin:
        type:
          - object
          - 'null'
        properties:
          name:
            type:
              - string
              - 'null'
          url:
            type:
              - string
              - 'null'
      species:
        type:
          - string
          - 'null'
      status:
        type:
          - string
          - 'null'
      url:
        type:
          - string
          - 'null'
    required:
      - id
    additionalProperties: true
"""
```

> [!Tip]
> You can use the Airbyte Cloud interface without costs to build your custom connector using the Connector Builder and copy the manifest.yaml from there to your PyAirbyte pipeline. 

```python
import yaml
from typing import cast

source_manifest_dict = cast(dict, yaml.safe_load(SOURCE_MANIFEST_TEXT))

source = ab.get_source(
    "source-rick-and-morty",
    config={},
    source_manifest=source_manifest_dict,
)
source.check()
source.select_all_streams()

result = source.read()

for name, records in result.streams.items():
    print(f"Stream {name}: {len(records)} records")
```

- `cast(dict,  yaml.safe_load(file))` turns the manifest string into a Python dict.
- `ab.get_source(...)` registers a *source‑rick‑and‑morty* connector from that manifest.
- `select_all_streams()` activates every stream defined in the YAML.
- `read(cache=cache)` executes the sync and writes the records into the same MotherDuck database used by the Stripe pipeline, so both datasets can be queried together.


### 4  Load records into a vector database

Structured analytics are valuable, but many projects call for semantic search. Below you embed each character record from the Rick & Morty API and store it in **Chroma‑DB**:

```python
%pip install chromadb
```

```python
import chromadb
from ast import literal_eval

chroma = chromadb.Client()
collection = chroma.create_collection("rick_and_morty")

rows = result["characters"].to_pandas().to_dict("index")

for row_id, row in rows.items():
    loc = literal_eval(row["location"])
    doc = f"""
    Name: {row['name']}
    Gender: {row['gender']}
    Species: {row['species']}
    Status: {row['status']}
    Location: {loc['name']}
    """
    collection.add(documents=[doc], ids=[str(row_id)])
```

Query the collection semantically:

- Each row is flattened into one **text string** because vector databases operate on embeddings of raw text; converting the JSON‑like record to prose lets the embedding model capture relationships between fields.
- We concatenate only the key attributes (name, gender, species, status, location) so the vector stays compact yet meaningful.
- `collection.add(...)` stores that string plus its embedding under the row‑id, making it searchable later.

```python
results = collection.query(
    query_texts=["Last Name is Smith"], # Chroma will embed this for you
    n_results=10 
)
for d in results.get('documents')[0]:
  print(d)
```

### What you accomplished

- **Durability** – Data now lives in MotherDuck and survives notebook restarts.
- **Security** – Secrets are fetched at runtime instead of hard‑coding keys.
- **Extensibility** – Any API can be ingested through a declarative manifest.
- **Vector search** – The same pipeline feeds a vector database for RAG and LLM workloads.

You now have a robust extraction flow that can power both analytical dashboards and AI‑driven applications.

