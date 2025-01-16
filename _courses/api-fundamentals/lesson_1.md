---
layout: lesson
title: Lesson 1 - Introduction to APIs
---

# Create Credentials
This will create the object has method to retrieve new and refresh the access token.
We don't need to do anything, now only provide the `client_id` and `client_secret`.

```python
from airbyte_api.models import SchemeClientCredentials

credentials = SchemeClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
    token_url="v1/applications/token"
)
```

# Second Step

The Airbyte API Reference documentation

To get credentials to make request to the API you must generate the access token.

Airbyte access token are short-lived (3 minutes) so it can be difficult to work with the API making manual requests.
Because of this we're going to show how to use the Python SDK later which handles the token refresh step automatically for us.

Here is how to get the access token using Postman.

Go to File → New Tab
Change request method from GET to POST
Page the url: https://api.airbyte.com/v1/applications/token
Click in the Body tab and change method from none to  method raw → JSON
After that click in Send

![github-search-sdk]({{ "/assets/images/api-fundamentals/github_sdk_search.png" | relative_url }})


We're going to receive the access_token necessary to run other commands throw the Airbyte API.
Copy the entire string for the field access_token and let's make our next request fast before it get expired.
