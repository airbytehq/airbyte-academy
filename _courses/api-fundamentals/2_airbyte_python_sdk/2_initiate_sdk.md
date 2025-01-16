---
layout: lesson
title: Lesson 2 - Initiate the SDK
---

### Create Client Credentials

This will create the object has methos to retrieve new and refresh the access token. We don't need to do anything, now only provide the `client_id` and `client_secret`.

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