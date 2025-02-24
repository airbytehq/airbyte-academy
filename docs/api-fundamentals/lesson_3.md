## Using the Airbyte API with Postman

### Create an Application

Go to the Settings (in left side panel) in **Airbyte Cloud** then click in **Applications**. After click in `Create an application` in the top right side of the page.

![image](https://hackmd.io/_uploads/BJjZQrc9Jx.png)

Provide a name, `airbyte-course` it is important as you can track what applications are requesting to the API.

The application will generate the `Client ID` and the `Client Secret` do not share them as it can expose your account.

### Generate the Access Token

The Airbyte API Reference documentation 

To get credentials to make request to the API you must generate the access token.

Airbyte access token are short-lived (3 minutes) so it can be difficult to work with the API making manual requests. Because of this we're going to show how to use the Python SDK later which handles the token refresh step automatically for us.

Here is how to get the access token using Postman.

1. Go to File → New Tab
2. Change request method from GET to POST
3. Page the url: <a href="https://api.airbyte.com/v1/applications/token" target="_blank">`https://api.airbyte.com/v1/applications/token`</a>
4. Click in the Body tab and change method from `none` to  method `raw` → `JSON`
5. After that click in Send

![image](https://hackmd.io/_uploads/H1gmXSc5Jx.png)


We're going to receive the `access_token` necessary to run other commands throw the Airbyte API. Copy the entire string for the field `access_token` and let's make our next request fast before it get expired.

1. Create a new request going to File → New Tab
2. Paste the `https://api.airbyte.com/v1/sources`
3. Click in Authorization tab and select Type `Bearer Token` 
4. Page the token from previous step
5. Click in `Send`

This will return all sources you have in all workspaces you have access. You can check the API reference documentation page to see all parameters available to configure and filter the request.

![image](https://hackmd.io/_uploads/Syt47Hc9Jl.png)

Resources:

- <a href="https://reference.airbyte.com/reference/createaccesstoken" target="_blank">Airbyte API Reference Documentation for Access Token Endpoint</a>

