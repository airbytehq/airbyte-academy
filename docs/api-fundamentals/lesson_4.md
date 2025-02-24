## Using the Python Airbyte API SDK

Now let's use a Google Colab Notebook to use Python to interact with Airbyte API 🐍.

Go https://colab.google and create a new notebook.

First let's add the `client_id` and `client_secret` as secrets in the notebook

![image](https://hackmd.io/_uploads/SJOr7B951e.png)

After copy the snippet to read the secrets in the notebook.

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

Now the variable `airbyte_api` can call any endpoint available in the API. Let's request the same as before to list all sources in our workspace.

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
# company test     00000000-5201-491d-1111-a1fd170df189
# user@company.com 00000000-2031-4a2f-1111-040a5d9c795c
```

This will print the workspace name and id your user have access.

Store this information as it will be needed later to create our first source.

```python
from airbyte_api.api import ListSourcesRequest

res = airbyte_api.sources.list_sources(
    request=ListSourcesRequest(
		    workspace_ids=[]
		)
)

for source in res.sources_response.data:
    print(source.name)
  
# Example of Output:  
# My Facebook Source
# Google Ads 1
# Convex
# Google Analytics 4 (GA4)
```

Now let's understand what happened here and how you can use the Python SDK to run other commands.

The `airbyte_api` has all endpoints available by the API. There are listed <a href="https://github.com/airbytehq/airbyte-api-python-sdk/tree/main?tab=readme-ov-file#available-resources-and-operations" target="_blank">here</a>.

Each method has an example of how to build their payload to run the command.

Let's do another example, now creating a new source.

1. Go to the method lists <a href="https://github.com/airbytehq/airbyte-api-python-sdk/tree/main?tab=readme-ov-file#available-resources-and-operations" target="_blank">documentation</a>
2. Search for `sources` → `create_source`
    1. You're going to this <a href="https://github.com/airbytehq/airbyte-api-python-sdk/blob/main/docs/sdks/sources/README.md#create_source" target="_blank">page</a>

The example provided in the documentation is quite complex to understand, so let's create a simpler one. But before let's break what we're going to need:

1. Create the Source model (in the example page is the `models.SourcePinterest`
2. Create the `SourceCreateRequest` model
3. Make the request to `create_source` method.

Let's create a new source using the Faker connector.

Use the left side search bar to find the connector documentation, type `sourcefaker`

![image](https://hackmd.io/_uploads/HyaDXB9ckg.png)


You must access the `docs/models/sourcefaker.md`

```python
from airbyte_api.models import SourceFaker

source_faker = SourceFaker(
    count=35
)
```

Faker have all optional fields with default values. In the example we override the `count` variable from `100` to `35`.

![image](https://hackmd.io/_uploads/SyI_QB9cJg.png)

Now let's create the `SourceCreateRequest`

```python
source_create_request = SourceCreateRequest(
    workspace_id='33b560c4-2de8-488d-be03-844f8e22ba0d',
    name="source_created_using_airbyte_api",
    configuration=source_faker
)
```

and then execute the api request

```python
airbyte_api.sources.create_source(source_create_request)
```

the output returned by the request is:

```bash
CreateSourceResponse(
content_type='application/json', 
status_code=200, 
raw_response=<Response [200]>, 
source_response=SourceResponse(
  configuration=SourceAirtable(
  credentials=None, 
  SOURCE_TYPE=<SourceAirtableAirtable.AIRTABLE: 'airtable'>), 
  name='source_created_using_airbyte_api', 
  source_id='0653df2b-67aa-4351-b50e-415e24939208', 
  source_type='faker', 
  workspace_id='33b560c4-2de8-488d-be03-844f8e22ba0d'
 )
)
```

