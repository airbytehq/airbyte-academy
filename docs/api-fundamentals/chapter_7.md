## Initiate the API

```python
from airbyte_api.models import Security
from airbyte_api import AirbyteAPI

airbyte_api = AirbyteAPI(security=Security(client_credentials=credentials))
```

Now the variable `airbyte_api` can call any endpoint available in the API. Let's request the same as before to list all sources in our workspace.

