# Using Airbyte Platform APIs to Build Data Pipelines

## Intro

Airbyte platform allows users to interact with it using an API this way users don't need to the UI.

This enables developers integrate Airbyte into their monitoring system, data pipeline or product.

The easiest way to interact with an API is using apps like Postman or running `curl` command directly in the terminal. 

For developers integrating the API using a Python or Java Airbyte a SDK to make it easier:

- Airbyte API Python SDK
- Airbyte API Java SDK

In this course we're going to show how to get credentials to run commands to the Airbyte API to execute commands for us using Postman and Python.

## Pre-reqs (Q)

1. Cloud account (works with both but URL different)
2. Postman - good for testing APIs
3. Collab notebook - this will be our IDE

## Using the Airbyte API with Postman

Go to the Settings (in left side panel) in Airbyte Cloud then click in Applications. After click in `Create an application` in the top right side of the page.

![image.png](Using%20Airbyte%20Platform%20APIs%20to%20Build%20Data%20Pipeline%201581b3df260c80dca55fc3b4eaeb82dc/image.png)

Provide a name, `airbyte-course` it is important as you can track what applications are requesting to the API.

The application will generate the `Client ID` and the `Client Secret` do not share them as it can expose your account.

## Generate the Access Token

The Airbyte API Reference documentation 

To get credentials to make request to the API you must generate the access token.

Airbyte access token are short-lived (3 minutes) so it can be difficult to work with the API making manual requests. Because of this we're going to show how to use the Python SDK later which handles the token refresh step automatically for us.

Here is how to get the access token using Postman.

1. Go to File → New Tab
2. Change request method from GET to POST
3. Page the url: [`https://api.airbyte.com/v1/applications/token`](https://api.airbyte.com/v1/applications/token)
4. Click in the Body tab and change method from `none` to  method `raw` → `JSON`
5. After that click in Send

![image.png](Using%20Airbyte%20Platform%20APIs%20to%20Build%20Data%20Pipeline%201581b3df260c80dca55fc3b4eaeb82dc/image%201.png)

We're going to receive the `access_token` necessary to run other commands throw the Airbyte API. Copy the entire string for the field `access_token` and let's make our next request fast before it get expired.

1. Create a new request going to File → New Tab
2. Paste the `https://api.airbyte.com/v1/sources`
3. Click in Authorization tab and select Type `Bearer Token` 
4. Page the token from previous step
5. Click in `Send`

This will return all sources you have in all workspaces you have access. You can check the API reference documentation page to see all parameters available to configure and filter the request.

![image.png](Using%20Airbyte%20Platform%20APIs%20to%20Build%20Data%20Pipeline%201581b3df260c80dca55fc3b4eaeb82dc/image%202.png)

Resources:

- [Airbyte API Reference Documentation for Access Token Endpoint](https://reference.airbyte.com/reference/createaccesstoken)

## Using the Python Airbyte API SDK

Now let's use a Google Colab Notebook to use Python to interact with Airbyte API 🐍.

Go [https://colab.google](https://colab.google) and create a new notebook.

First let's add the `client_id` and `client_secret` as secrets in the notebook

![image.png](Using%20Airbyte%20Platform%20APIs%20to%20Build%20Data%20Pipeline%201581b3df260c80dca55fc3b4eaeb82dc/image%203.png)

[data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAclBMVEVHcEzxjQX5qQDzlgT0lwLzlwT5qgD5qwD5qwD5qwD5qwD5qgDwjAX5qwD5qAD5qwD5qwD5qwD0mQPregj3pQHwjwbocQrocQruhgf5qgDwjAbocQrocQrpcQr5qwDocQrrfAjpcgnpcQnpcgnwjQbwjAZUryHnAAAAJnRSTlMADjMmBhyS1fDnw2wV4K9M+P8+l/6vdfb8Xff/hN176DO+aVPn4zRFwdUAAAEASURBVHgBzVEFtsMwDEuZmRtO/r//FWfPHZ5gKvlJjUzsRxGEYRRTGEdhmLxJYZrleVFWNfxVlUWeN213SXXaD4QsGbPhQhvdtWl+El0xPDAv6L1u+zwUZZn1zVEi3TdNPswnFzGLJOd72yVJqKoUtUx149GenGvDVs65NVRmiVqHVUcWaMHgvTmqbCzAU1HsNjjDwFWORBz5MDRX7DX4fotZdIkb8N+2BXUfTFjKd0F9WqPmNNDrs5WaWpn/Jj/6CTUZMTgKQ2jKloaA/UmU+LaCRfI+vn/+xFQzVJ+DbyJjOWETqCHGtMGVqQRK8YvU2grqiFDDsoNHnCQx+03cADN4Gl+iZEmCAAAAAElFTkSuQmCC](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAclBMVEVHcEzxjQX5qQDzlgT0lwLzlwT5qgD5qwD5qwD5qwD5qwD5qgDwjAX5qwD5qAD5qwD5qwD5qwD0mQPregj3pQHwjwbocQrocQruhgf5qgDwjAbocQrocQrpcQr5qwDocQrrfAjpcgnpcQnpcgnwjQbwjAZUryHnAAAAJnRSTlMADjMmBhyS1fDnw2wV4K9M+P8+l/6vdfb8Xff/hN176DO+aVPn4zRFwdUAAAEASURBVHgBzVEFtsMwDEuZmRtO/r//FWfPHZ5gKvlJjUzsRxGEYRRTGEdhmLxJYZrleVFWNfxVlUWeN213SXXaD4QsGbPhQhvdtWl+El0xPDAv6L1u+zwUZZn1zVEi3TdNPswnFzGLJOd72yVJqKoUtUx149GenGvDVs65NVRmiVqHVUcWaMHgvTmqbCzAU1HsNjjDwFWORBz5MDRX7DX4fotZdIkb8N+2BXUfTFjKd0F9WqPmNNDrs5WaWpn/Jj/6CTUZMTgKQ2jKloaA/UmU+LaCRfI+vn/+xFQzVJ+DbyJjOWETqCHGtMGVqQRK8YvU2grqiFDDsoNHnCQx+03cADN4Gl+iZEmCAAAAAElFTkSuQmCC)

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

## Create Client Credentials

This will create the object has methos to retrieve new and refresh the access token. We don't need to do anything, now only provide the `client_id` and `client_secret`

```python
from airbyte_api.models import SchemeClientCredentials

credentials = SchemeClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
    token_url="v1/applications/token"
)
```

## Initiate the API

```python
from airbyte_api.models import Security
from airbyte_api import AirbyteAPI

airbyte_api = AirbyteAPI(security=Security(client_credentials=credentials))
```

Now the variable `airbyte_api` can call any endpoint available in the API. Let's request the same as before to list all sources in our workspace.

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

The `airbyte_api` has all endpoints available by the API. There are listed [here](https://github.com/airbytehq/airbyte-api-python-sdk/tree/main?tab=readme-ov-file#available-resources-and-operations).

Each method has an example of how to build their payload to run the command.

Let's do another example, now creating a new source.

1. Go to the method lists [documentation](https://github.com/airbytehq/airbyte-api-python-sdk/tree/main?tab=readme-ov-file#available-resources-and-operations)
2. Search for `sources` → `create_source`
    1. You're going to this [page](https://github.com/airbytehq/airbyte-api-python-sdk/blob/main/docs/sdks/sources/README.md#create_source)

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