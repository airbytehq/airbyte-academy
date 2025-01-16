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

