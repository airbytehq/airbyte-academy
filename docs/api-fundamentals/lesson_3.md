## Get the API Credentials

### Create an Application

Go to the Settings (in left side panel) in **Airbyte Cloud** then click in **Applications**. `Create an application` on the top right side of the page.

![image](https://hackmd.io/_uploads/BJjZQrc9Jx.png)

Provide a name, today, we’ll call our application `airbyte-course`  – this is important for you to  track what applications are making requests to the API.

The application will generate the `Client ID` and the `Client Secret`.

> [!Warning]
> Do not share them as it can expose your account data and connectors.

### Generate the Access Token

To get credentials to make a request to the API you must generate the access token.

Airbyte access tokens are short-lived, lasting only 15 minutes. However, during this brief period, we can conduct manual tests to validate our credentials.

In the Applications page, after creating your application, you can generate an access token directly in the UI. This feature is useful for running one-time commands, which is exactly what we're looking for.

![image](https://hackmd.io/_uploads/HJcrPQ_aJg.png)

Click **Generate access token** and Copy the content of the result.

![image](https://hackmd.io/_uploads/rk3yuXdaJg.png)

Ok, now we have our access token. You should save this in a secure location. We will need to paste it later in Postman and curl. Let's proceed with our first request.

> [!Tip]
> If you lose the access token or it has expired, you can regenerate a new one.

### Making the First API Request


Now let's do our first request.
Access the <a href="https://reference.airbyte.com/reference/listworkspaces" target="_blank">Airbyte API Page `ListWorkspace` endpoint</a>.

Paste the token Bearer field.
![image](https://hackmd.io/_uploads/S1HwimOaJe.png)

Now click in **`Try it!`** and check the results!
![image](https://hackmd.io/_uploads/ByJl3QOp1x.png)

Congratulations! You have made your first request to the Airbyte API.

This is truly amazing, but it can be frustrating. You need to regenerate the token every 15 minutes and navigate page by page to complete a task. That's why we will use the Python SDK to automate this process for us.


