## Build a Pipeline using the Python SDK and Airbyte API

Now let's use a Google Colab Notebook to use Python to interact with Airbyte API 🐍.

Go https://colab.google and create a new notebook.

You can find this information in the Airbyte Cloud -> Application Page
![image](https://hackmd.io/_uploads/BJ0dTXO6Jl.png)

Copy the `Client ID` and `Client Secret` to the Google Colab Notebook.
Create a variable called `AIRBYTE_CLIENT_ID` and `AIRBYTE_CLIENT_SECRET`

![image](https://hackmd.io/_uploads/SJOr7B951e.png)

After copy the provided snippet to read the secrets in the notebook.

Now let's install the Python library to execute the commands.

Your notebook should look like this:

```bash
!pip install airbyte-api
```

```python
from google.colab import userdata
client_id = userdata.get('AIRBYTE_CLIENT_ID')
client_secret = userdata.get('AIRBYTE_CLIENT_SECRET')
```

After running the pip install let's create a credential object is going to help us refresh the token when it got expired.

### Create Client Credentials

This will create the object has methos to retrieve new and refresh the access token. We don't need to do anything, now only provide the `client_id` and `client_secret`

```python
from airbyte_api.models import SchemeClientCredentials

credentials = SchemeClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
    token_url="v1/applications/token"
)
```

### Initiate the API

```python
from airbyte_api.models import Security
from airbyte_api import AirbyteAPI

airbyte_api = AirbyteAPI(security=Security(client_credentials=credentials))
```

Now the variable `airbyte_api` can call any endpoint available in the API. Let's do the same request we made before to list workspaces.

### Making our first request using Python SDK

```python
from airbyte_api.api import ListWorkspacesRequest

res = airbyte_api.workspaces.list_workspaces(
    request=ListWorkspacesRequest()
)

for workspace in res.workspaces_response.data:
    print(workspace.name, workspace.workspace_id)

# Example output
# workspace 1      00000000-360f-4ffc-1111-2507f8337b3d
```

Create a variable called `wid` and attribute the `uuid` for your workspace. See image:
![image](https://hackmd.io/_uploads/BJYYqr_p1l.png)

> [!Important]
> You didn't need to create an`access token`. It was managed by the code itself. Awesome right?

### Create a Source

Now, let's create a source to connect to a destination and transfer some data. We'll use a mock source, but this example can easily be applied to the entire catalog.


For Source Faker you can check <a href="https://github.com/airbytehq/airbyte-api-python-sdk/blob/main/docs/models/sourcefaker.md" target="_blank">this documentation</a> describe all required and optional fields.

> [!Tip]
> You can search all source and destination configurations <a href="https://github.com/airbytehq/airbyte-api-python-sdk/tree/main/docs/models" target="_blank">here</a> than in the search bar search for `sourcefaker`, `destinationmother`.
> Click in the `.md` file inside the `airbyte-api-python-sdk/docs/models` folder.


```python
from airbyte_api.models import SourceFaker, SourceCreateRequest

source_faker_config = SourceFaker(
    connection_type="faker",
    count=35
)
req = SourceCreateRequest(
    configuration=source_faker_config,
    name='my_source_faker_using_api',
    workspace_id=wid,
)
res = airbyte_api.sources.create_source(request=req)

source_id =  res.source_response.source_id
print(source_id)
```
1. `source_faker_config`: create the configuration object. Think as this step as populating the field of the image below in the UI
![image](https://hackmd.io/_uploads/HJOAjrupyl.png)
2. `req`: Send the  the payload to send to the API. Now we inform what is the workspace we want to create the source.
3. `res`: make the actual request to the Airbyte API
4. `source_id`: reads the output of `res` and store the source id necessary to create a connection later.

The complete `res` response object is:
```
CreateSourceResponse(
    content_type='application/json', 
    status_code=200, 
    raw_response=<Response [200]>, 
    source_response=
        SourceResponse(
            configuration=SourceAirtable(
                credentials=None, 
                SOURCE_TYPE=<SourceAirtableAirtable.AIRTABLE: 'airtable'>), 
                created_at=1743441021, 
                definition_id='dfd88b22-b603-4c3d-aad7-3701784586b1', 
                name='my_source_faker_using_api', 
                source_id='e1ee0c87-faeb-438c-858d-3bcb813152fb', 
                source_type='faker', 
                workspace_id='1da6a888-9115-4431-9ded-ff0a42b10598'
        )
)
```

Go the Airbyte Source Page and check your new source!

### Create a Destination

For our destination we're going to use Motherduck. It offers a 21 free days trial and have a nice UI to check our data later.
Create an account <a href="https://motherduck.com/" target="_blank">here</a>.

After you have created your account create the databse it will receive the data. Click in `+` right side of Attached databases sidebar. Let's call `lms`
![image](https://hackmd.io/_uploads/Byn9GUuaJg.png)

![image](https://hackmd.io/_uploads/SyJuGUOaye.png)

Now, let's go to Seetings (right top corner) -> Secrets -> Access Token. The same you made with Airbyte.
![image](https://hackmd.io/_uploads/SyIc6r_T1l.png)

Copy the token and return to the Collab Notebook and create a new secret.
Call the new secret of `MOTHERDUCK_APIKEY`
![image](https://hackmd.io/_uploads/HJJn6S_ayx.png)

Check all parameter configuration for Destination MotherduckDb <a href="https://github.com/airbytehq/airbyte-api-python-sdk/blob/main/docs/models/destinationmotherduck.md" target="_blank">here</a>

```python
from airbyte_api.models import DestinationDuckdb, DestinationCreateRequest

md_apikey = userdata.get('MOTHERDUCK_APIKEY')

duckdb_config = DestinationDuckdb(
    destination_path="md:lms",
    motherduck_api_key=md_apikey
)
req = DestinationCreateRequest(
    configuration=duckdb_config,
    name='my_duck_using_api',
    workspace_id=wid,
)

res = airbyte_api.destinations.create_destination(request=req)

destination_id = destination_res.destination_response.destination_id
print(destination_id)
```
1. `md_apikey`: read the access token from Collab Secrets.
2. `duckdb_config`: create the configuration for the destination, in this case we're sending data to `md:lms` database in motherduck.
3. `req`: build the payload to create the destination.
4. `res`: make the request and return the result.
5. `destination_id`: stores the destination id generated in the previous request. We're going to use to create the connection.

Ok now we have both source and destination created. It is time to connect them together and trigger a sync!

### Create a Connection

```python
from airbyte_api.models import ConnectionCreateRequest

connection_config = ConnectionCreateRequest(
    name="my_connection_using_api",
    source_id=source_id,
    destination_id=destination_id,
)

res = airbyte_api.connections.create_connection(
    request=connection_config
)

connection_id = res.connection_response.connection_id
```
1. `connection_config`: create the payload configuration for a connection. This is an example connect our source to destination, keep the schedule as manual and do not change any field or namespace.
2. `res`: make the request
3. `connection_id`: stores the id to trigger the sync in the next step.


### Run a sync using the API
```python
from airbyte_api.models import JobCreateRequest, JobTypeEnum

req = JobCreateRequest(
    connection_id=connection_id,
    job_type=JobTypeEnum.SYNC,
)

res = airbyte_api.jobs.create_job(
    request=req
)

print(res)
```
1. `req`: create the payload to trigger a sync it requires the `connection_id` and the type of sync `SYNC` to ingest data or `RESET` to delete data.
2. `res`: if everything runs without problem it will return an object with status code 200.

That's it! Check the Airbyte UI and see your first data ingestion trigger by the API.

![image](https://hackmd.io/_uploads/HyjCPUdpkg.png)


