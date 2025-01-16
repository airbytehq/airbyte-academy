---
layout: lesson
title: Lesson 1 - Introduction to APIs
---

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
