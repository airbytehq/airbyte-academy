---
layout: lesson
title: Lesson 1 - Using the Python Airbyte API SDK
---

Now let's use a Google Colab Notebook to use Python to interact with Airbyte API 🐍.
Go https://colab.google and create a new notebook.
First let's add the `client_id` and `client_secret` as secrets in the notebook.

![image]({{ "/assets/images/api-fundamentals/collab_secrets.png" | relative_url }})

After copy the snippet to read the secrets in the notebook.
Now let's install the Python library to execute the commands.
Your notebook should look like this:

```shell
!pip install airbyte-api
```

```python
from google.colab import userdata
client_id = userdata.get('AIRBYTE_CLIENT_ID')
client_secret = userdata.get('AIRBYTE_CLIENT_SECRET')
```

After running the pip install let's create a credential object is going to help us refresh the token when it got expired.
