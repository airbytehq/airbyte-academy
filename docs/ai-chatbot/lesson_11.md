## The AI Chatbot
Duration: 0:20:00

You will create the AI chatbot in Python. To make things simple, we will use a Google Collab notebook. You can think of this as an online IDE. Go ahead and navigate to [Google Collab](https://colab.research.google.com/) and create a new notebook called airbyteai. If you would prefer to follow along, here is [a completed notebook](https://colab.research.google.com/drive/1B8QXrUGPi5JvjOwVREoGdAK72AJyU5fy#scrollTo=HVDlskc0S6ry) for you.

:::info
At the end of each step, don't forget to tap the Run button beside the code to have Collab execute it for you.
:::

### Add Required Libraries
Install the required libraries.

```
pip install supabase; openai

```
Then, import everything into your project space. 

:::info
You may notice that we didn't import os. This is automatically available in the collab notebook. 
:::

```
import os
from supabase import create_client, Client
import openai
```

### Configure Supabase Client
We need to configure the supabase client using the URL and Client key that we previously used in the Airbyte Destination Configuration. To keep things secure, we want to use secrets. If you are not using a Collab notebook, I encourage you to use their environment variables or a .env file to avoid hardcoding sensitive information in your app. 

Within Collab, tap the key icon on the left, and add two secrets. Both of these may be obtained within Supabase via Settings > Configuration > API 
python.

- SUPABASE_URL
- SUPABASE_KEY
 
![CleanShot 2024-12-23 at 13.10.04](https://hackmd.io/_uploads/By5a-LDHyx.png)

Now, configure your client

```
from google.colab import userdata

url = userdata.get('SUPABASE_URL')
key = userdata.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)
```

::: info
When you tap run, if this is your first time accessing the keys, you will be prompted to grant access to the secrets. This is ok. Accept and continue.
:::

### Configure OpenAI 
Just like we did with Supabase, we need to add the OpenAI API key. G, OPENAI_API_KEY, add it to your code. To obtain an OpenAI API key, log into your OpenAI account, tap the cog icon in the upper right, then API Keys from the left hand menu, and finally tap Create New Secret Key. 

![CleanShot 2024-12-23 at 16.55.35](https://hackmd.io/_uploads/HJ_WwFPBJe.png)


Copy the key and create another secret in your Collab notebook. Then, we can reference it in our code.

```
openaikey = userdata.get('OPENAI_API_KEY')
```

### Create Embeddings
Next, we need to write a helper function to take the input question from the user and get openAI to convert it into an embedding. We are going to use the text-embedding-3-small model. You can experiment with others, but this works great for our requirement.

```
# Function to get embedding vector for a question using OpenAI
def get_question_embedding(question):
    response = openai.embeddings.create(input=question, model="text-embedding-3-small")
    return response.data[0].embedding
```
### Pass the Question to the right context (table)
Now that we have a question, we need to ask the question against the correct dataset. This way, we can compare the embedding of the question against the embeddings of each row. To do this, let's create a simple if, else statement looking for context in the question. Specifically, we will look for a keyword that matches one of the tables that are part of the Airbyte sync job: customer, product, or invoice. 

You will see that our calls to Supabase are using the functions we created earlier, and take the question_vector as the input parameter.

```
def get_context(question) -> str:
    # Get embedding for the question
    question_embedding = get_question_embedding(question)
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

### Handle Responses
All that is left is to handle the response to a question. Thankfully, openAI does all the heavy lifting for it. We just need to set up the prompt, and tell openAI which model to use and how many tokens to apply against my account. 

```
# Function to get AI response using OpenAI's chat completion
def get_response(question: str):
    openai.api_key = openaikey
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


### Test it
All that is left to do is write a quick test, run it and see our hard work pay off!

TODO: CONFIRM YOU CAN DO THIS ON A FREE PLAN. SHOULD AS LONG AS YOU HAVE TRIAL CREDITS

TODO: make more test. things like:
 - what is the most common product sold?
 - when someone buys more than one product, what is the most common second product sold?
 - who made the cheapest purchase? How much did they pay, and what did they buy?
 - what is the most common purchase that women make?

```
# Example usage
question = "Is there a customer named Justin? If so, show me his information"
answer = get_response(question)
print("Answer:", answer)
```
![CleanShot 2024-12-23 at 17.14.56](https://hackmd.io/_uploads/HJlrsKwSkl.png)

Congratulations! You have successfully built your AI chatbot powered by Airbyte.


