## Making our first request using Python SDK

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

![image.png](Using%20Airbyte%20Platform%20APIs%20to%20Build%20Data%20Pipeline%201581b3df260c80dca55fc3b4eaeb82dc/image%204.png)

You must access the `docs/models/sourcefaker.md`

```python
from airbyte_api.models import SourceFaker

source_faker = SourceFaker(
    count=35
)
```

Faker have all optional fields with default values. In the example we override the `count` variable from `100` to `35`.

![image.png](Using%20Airbyte%20Platform%20APIs%20to%20Build%20Data%20Pipeline%201581b3df260c80dca55fc3b4eaeb82dc/image%205.png)

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

Tcharam 😎