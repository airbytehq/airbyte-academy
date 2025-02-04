## The AI Chatbot

Finally, it is time to create the AI chatbot in Python. To make things simple, we will use a Google Collab notebook. You can think of this as an online IDE. Go ahead and navigate to <a href="https://colab.research.google.com/" target="_blank">Google Collab</a> and create a new notebook called airbyteai. If you would prefer to follow along, here is <a href="https://colab.research.google.com/drive/1jVFNDFV3JyYWEGj_iTQo0cDjIYzM4aTM" target="_blank">a completed notebook</a> for you.

>[!NOTE]
> At the end of each step, don't forget to tap the Run button beside the code to have Collab execute it for you.


### Add Required Libraries
Install the required libraries.

```bash
!pip install -qU langchain-core openai supabase
```

Then, import everything into your project space.

```python
import os
import openai
from supabase import create_client, Client
from langchain_core.embeddings import DeterministicFakeEmbedding
```
We will again be using the Fake Embeddings model from Langchain simply to save on cost and for testing purposes.

### Configure Environment Variables
We need to configure the Supabase client using the URL and API key. To obtain these, from within Supabase tap Settings > API settings. You need the Project URL and Project API key



To keep things secure, we want to use secrets. If you are not using a Collab notebook, we encourage you to use their environment variables or a .env file to avoid hardcoding sensitive information in your app. 

Within Collab, tap the key icon on the left, and add the following key/value pairs:

- `SUPABASE_URL`
- `SUPABASE_KEY`
 
![CleanShot 2024-12-23 at 13.10.04](https://hackmd.io/_uploads/By5a-LDHyx.png)

Just like we did with Supabase, we need to add the OpenAI API key. To obtain an OpenAI API key, log into your OpenAI account, tap the cog icon in the upper right, then API Keys from the left hand menu, and finally tap Create New Secret Key. Remember to copy the key immediately. You can not go back and retrieve it later. 

- `OPENAI_API_KEY`

![CleanShot 2024-12-23 at 16.55.35](https://hackmd.io/_uploads/HJ_WwFPBJe.png)

Copy the key and create another secret in your Collab notebook.

### Configure Supabase Client
Now that all our environment variables are set, we need to use them to configure the client and make the OpenAI key available when we call the API

```python
from google.colab import userdata

url = userdata.get('SUPABASE_URL')
key = userdata.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)


```

>[!NOTE]
> When you tap run, if this is your first time accessing the keys, you will be prompted to grant access to the secrets. This is ok. Accept and continue.

So far, your code should look like the following:

```python=
import os
import openai
from langchain_core.embeddings import DeterministicFakeEmbedding
from supabase import create_client, Client
from google.colab import userdata

# Access env variables
url: str = userdata.get('SUPABASE_URL')
key: str = userdata.get('SUPABASE_KEY')
api_key: str = userdata.get('OPENAI_API_KEY')
openapi.api_key = api_key


# Initialize Supabase client
supabase: Client = create_client(url, key)

```

>[!NOTE]
> Quick note on the OpenAI API Key. The variable name we set for the key, ``api_key``, is very important. It will throw errors if you try to run this with a different variable name so just something to be aware of.

### Initialize the text embeddings model
Now we'll need to setup the text embedding model to turn our user's question in vectors. We can do this simply with the following code:

```python
embeddings = DeterministicFakeEmbedding(size=1536)
```
Ensure that the dimension size of the embedding model is set to ``1536``. This matches the chunk size we set at the destination level of Airbyte.

### Creating the Context
We now need to create the context for our model to eventually use and generate a response. To do that we need to make a function that does the following:

* Embeds our user's question
* Takes those embeddings and calls the apropriate function based on the question asked
* Returns data with the closest vector distance that answers the question

The function will look like this:

```python
def get_context(question: str) -> str:
    # Embed the user's question
    question_embedding = embeddings.embed_query(question)
    
    results = []
    
    # Determine which table to query based on keywords in the question
    if "customer" in question.lower():
        query = supabase.rpc("find_related_customer", {'question_vector': question_embedding}).execute()
    elif "product" in question.lower():
        query = supabase.rpc("find_related_products", {'question_vector': question_embedding}).execute()
    elif "invoice" in question.lower():
        query = supabase.rpc("find_related_invoices", {'question_vector': question_embedding}).execute()
    else:
        return "No relevant context found for the given question."

    # Process query results
    for item in query.data:
        results.append(item)

    return results
```
You'll notice that depending on the keywords found in the question, we use Supabase's RPC method to call the Postgres functions we created earlier using the question embeddings as the argument we pass in. 

### Generate a Response
All that is left is to pass our context to the LLM and get a generated response. Thankfully, OpenAI does all the heavy lifting. We just need to set up the prompt, and tell OpenAI which model to use and how many tokens to apply against my account. 



```python!
# Function to get AI response using OpenAI's chat completion
def get_response(question: str):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about the customers, products, and invoices provided to you in the context. Use only the provided context to answer questions. If the information isn't in the context, say so."},
            {"role": "user", "content": f"Question: {question}\n\nContext:\n{get_context(question)}"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
```

>[!NOTE]
>We are using the gpt-4o-mini model from OpenAI. You will need to ensure that your OpenAI project is configured to allow it's use. By default, all models are allowed in the free tier, but to be safe, we want to explictly allow it via OpenAI > Settings > Project > Limits > Edit > add a check beside gpt-4o-mini and save. 

### Test it
All that is left to do is write a quick test, run it and see our hard work pay off!

>[!NOTE]
> OpenAI requires tokens/credits to run similarity searches. Free plans should be sufficient to run and complete this course, but please check your balance if you have used up free credits in other projects. 


```python
# Example usage
question = "Is there a customer named Justin Chau? If so, show me his information"
answer = get_response(question)
print("Answer:", answer)
```
![CleanShot 2024-12-23 at 17.14.56](https://hackmd.io/_uploads/HJlrsKwSkl.png)



