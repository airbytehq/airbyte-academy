# Build an AI Chatbot

## Overview 
From chatbots to large language models it seems AI is everywhere. Developer tools and platforms are moving at an incredible pace making it possible for anyone with some coding skills to build highly complex AI-driven apps in a short amount of time. At the heart of any AI application is access to the right data. The Airbyte platform is a core aspect of building the right AI data stack to unlock data, whether it is structured or unstructed and make it available for AI use cases.   

In this tutorial, you will build an AI-powered chatbot to allow users to interact with e-commerce data. They will be able to ask natural language questions to uncover insights in the data. 



### What You Will Learn
In this tutorial, you will learn the following how to deploy, configure, and create an AI+data full stack application. 

![aichatnew](https://hackmd.io/_uploads/SJ1FeFAdyg.png)



You will get hands on with:

- Airbyte Cloud to connect to Stripe test data
- Use the Airbyte Postgres Destination connector to send Stripe data to Postgres, deployed on Supabase
- Configure Supabase to use PGVector to support embeddings
- Create a data pipeline in Airbyte to handle sync tasks and send data embeddings for AI use cases 
- Create SQL functions to work with openAI question embeddings
- Write python-based chatbot uses OpenAI APIs to interact with your data and embeddings.
- (bonus) Create a full-stack web application with a frontend in Next.js, to host your chatbot

Whilst a basic understanding of coding in Next.js, Python, and SQL is helpful, if you are not comfortable with coding in these languages, don't worry! All of the code will be provided for you throughout.



## Pre-requisites

To get started, you will need to set up the following accounts. Lucky for you - you can complete this entire course using free or trial versions. You will not require a credit card or paid account. 

1. Stripe: Stripe is a very popular platform for processing online payments, with great developer APIs. You will need to [Sign up](https://dashboard.stripe.com/register) for Stripe account. This will allow you to access test Stripe data for users, products, invoices, and purchases. You do not need to add any payments information. You can skip this during the setup.
2. Airbyte Cloud: Airbyte will be used as the data movement platform connecting Stripe with a modern database like Postgres to enable RAG applications. You will use a 14-day trial of Airbyte Cloud. You can [sign up here](https://cloud.airbyte.com/signup?utm_medium=lms&utm_source=course-ai). If you already have an Airbyte Cloud account, please feel free to use this. 
3. Supabase: Supabase is a cloud-based backend-as-a service. At it's core, it is a managed PostgresSQL database. We will use this database, with the PGVector extension to build a RAG application. [Sign up here](https://supabase.com/dashboard/sign-in) and create an empty project, giving it whatever name you like. Make sure you write down the database password. You will need later.
4. OpenAI: OpenAI, the makers of ChatGPT provide an API platform for developers to build solutions with natural language processing and similarity search. [Sign up for a free account.](https://platform.openai.com/) You will use this for your chatbot to perform searches on your data using the [Chat Completion API](https://platform.openai.com/docs/api-reference/chat).   
5. Google Account: You will create the chatbot code in Python using a Google Collab notebook. In order to do so, you will need a [free gmail account](https://accounts.google.com/lifecycle/steps/signup/name). If you prefer to code locally, in your favorite IDE instead of a collab notebook, please do so, just keep in mind, this tutorial will not cover local Python environment configuration. 

Once you have created all of your accounts. Let's continue.



## A Quick AI Terminology Primer

There are a lot of new terms when working with AI. They can be overwhelming, but they don't have to be. Here is a quick primer on the most important things you need to understand. Throughout this tutorial, you will apply many of these techniques in your app. 

1. **RAG** (Retrieval-Augmented Generation) is an AI architecture which can produce accurate and relevant outputs. In this tutorial, RAG will be used to allow the end user to ask questions such as "what are the most popular products sold?". RAG relies on three key technologies: the retrieval system (for this example, embeddings), model (for this example, openAI's LLM), and vector embeddings (for this example, via PGVector)
2. **LLM**: An LLM (Large Language Model) is a type of artificial intelligence model designed to understand and generate human-like text. It is trained on massive datasets of text from diverse sources and uses advanced machine learning techniques to process and generate language. In this tutorial, we will use OpenAI's LLM.
3. **Embeddings**: Embeddings are a type of representation that transforms data (such as text, images, or other inputs) into dense, low-dimensional vectors of numbers. This makes it easier to perform searches against the data, as it is comparing numbers. 
4. **Similarity** **search**: Similarity search is a technique used to find data items that are most similar to a given query item. It is widely applied in tasks where the goal is to retrieve or rank items based on their similarity in content, context, or structure. It is performed against embeddings. 
5. **Hallucinations**: A hallucination refers to a scenario where a generative model, such as a large language model (LLM) that looks correct but factually incorrect, logically flawed, or completely fabricated. The best way to avoid hallucinations is to provide LLMs with domain-specific data. In this case, the data we will provide the LLM will come from Stripe.



With a primer on key terminology out of the way, it is time to start building your app.

## Configure Stripe

[Log into the  Stripe account](https://dashboard.stripe.com/test/dashboard) that you create earlier. make sure that you see the orange Test mode banner at the top. This means you are working with test data and no payment processing will occur. If you do not see this, please click the test mode toggle on the upper right. 

Once you have your Stripe environment in Test mode, tap Developers in the lower left, then select API keys. Copy the Secret key. You will need this in the next step.
![CleanShot 2025-01-14 at 10.06.45@2x](https://hackmd.io/_uploads/rJECw7Ewke.png)


### Load Test Data

A chatbot is pretty boring without data. We will be retrieving data from Stripe for products, customers, and purchases. To save some time, we have created a  [python script](https://colab.research.google.com/drive/1hozY9eZ3g37NtBwBU1hDVujfJtfrpW-5?usp=sharing//) to load test data. From within, the Colab notebook. You will see 3 steps in the collab notebook: 
1. Add a secret key (tap on the key icon on the left) ``STRIPE_TEST_KEY`` and use the value from the previous section. 
1. Install the Stripe library
1. Run the script to create and insert test data.
![CleanShot 2025-01-14 at 10.08.32@2x](https://hackmd.io/_uploads/BypNumNDJl.png)

When you run the script, watch for the debug output. Ensure that you see a line which says *Sample data creation complete.* 

## Configure Supabase
We are going to use Supabase as the backend and database portion of the chatbot. You should have already completed the pre-requisites and have a Supabase account. If not, [please create one now](https://supabase.com/dashboard/sign-up). 

Once logged in, if you haven't created a Project already, tap *New Project* and select the Organization which you created previously. Name the project, "AirbyteAIBot" and Tap "Create new project".

> [!NOTE]
> If you can not name your project upon initial set up, you can always do it later. Don't worry, the name is not important for any of the code we will write.

Once your project is created, there are a few important things to note, especially when creating Destination connectors from Airbyte, in particular, Project URL and API Key. You will need these shortly. You can always access these keys, via Settings > API (under Configuration) if you need them.

![CleanShot 2024-12-23 at 11.54.55](https://hackmd.io/_uploads/B1VSgBPSJg.png)

Supabase automatically creates a database on your behalf. Tapping on the database icon on the left navigation, and ensuring you have the public schema selected, Supabase currently shows no tables have been created yet. Don't worry, these will be automatically created by Airbyte when you sync data for the first time. 
![CleanShot 2024-12-23 at 12.04.41](https://hackmd.io/_uploads/SJB9zHPr1x.png)

### Enable PGVector Extension
One thing you do need to do is enable PGVector. PGVector is an extension to Postgres to allow it to create and store embeddings. Tap Extensions in the database submenu, and type "PGVector" into the search box, then enable the extension via the toggle. 

![CleanShot 2024-12-23 at 12.07.54](https://hackmd.io/_uploads/r1rI7HwH1e.png)




## Create Source Connector & Streams

Now that we have our database and other environments all set up, we know the source of the data (Stripe) and where we want to move the data, or destination (Postgres on Supabase). It is time to create the data pipeline which will move the data. For this, we will use the Airbyte Cloud platform. To get started, you will need access to your [Airbyte credentials](https://cloud.airbyte.com?utm_medium=lms&utm_source=course-ai), and we will establish our connection first. 

Within Airbyte, tap Builder in the left menu, then New custom Connection.

![airbytecircles](https://hackmd.io/_uploads/SJvp6IDrJl.png)

You will be presented with options to create your connector. Select Start from Scratch. 

We're starting from scratch to have complete control over our API configuration and to precisely define what Stripe data we want to include in our AI pipeline. We will call the Source Connector "StripeCustomerData"



![startfromscratch ](https://hackmd.io/_uploads/SJrdn8PBJg.png)

>[!NOTE]
> Airbyte offers a pre-built Stripe connector. We could have used this in the tutorial, but wanted to get you hands-on with the connector builder, and it allows us more control over specific fields that we want to sync.


We'll use manual connector setup rather than the AI Assistant. This method works best when you need precise control over your API data collection.

![manually](https://hackmd.io/_uploads/rJytCIPHJg.png)

For the base URL, you can use https://api.stripe.com, and Bearer token is used here for Auth: 
![stripeurl](https://hackmd.io/_uploads/HkxjyDwSyx.png)

If you click on the "Testing Values" button on the top right, you can see where to put your Stripe API key. Using the [secret API key](https://dashboard.stripe.com/test/apikeys) in test mode will probably be the best way to do this. 

![stripeapikey](https://hackmd.io/_uploads/SylfWDvSkl.png)

Now that we have the global configuration setup, let's tackle the actual data streams: 

We have four streams in this tutorial that capture the most useful data: 
- Customers
- Search Customer
- Invoices
- Products


### Customers

To set up the Customer Stream, see the [customers endpoint](https://docs.stripe.com/api/customers) - /v1/customers. This is of course, our URL path! Click the plus button to get started: 

![customer-stream-setup](https://hackmd.io/_uploads/ByYWfvvryl.png)

We are sending a ``GET`` request and getting JSON as the response. Record selector is selected here which is essential for filtering the records of data. 

![customers](https://hackmd.io/_uploads/SJ5YsFCOke.png)

Tap the test button to ensure everything is working before moving on.

### Search Customer

For the search customer stream, you can use - [/v1/customers/search ](https://docs.stripe.com/api/customers/search//)as the endpoint. This endpoint takes a query parameter, query and an email in the form of email:"theemail@address.com". If you want to add an email to test, simply tap the Add button beside query parameter using an email created during the Stripe data load. (You an retrieve these by tapping on Customers on the left hand navigation in Stripe) Then, tap Test. 

![search-customer-stream](https://hackmd.io/_uploads/rJTpuTjHkl.png)

### Invoices

Use [/v1/invoices](https://docs.stripe.com/api/invoices//) for the endpoint. Toggle "Use an existing stream configuration" on and select Customers. This will copy over configuration for things like the record selector. 

### Products

Use [/v1/products](https://docs.stripe.com/api/products//) for the endpoint. Toggle "Use an existing stream configuration" on and select Customers. This will copy over configuration for things like the record selector. 



After building the streams, we can publish the custom connector. Now we just need to build the final connection! Click "Publish" on the top right corner, giving it a name "Stripe-to-Supabase"

![connector-published](https://hackmd.io/_uploads/rywatyhryx.png)

>[!NOTE]
>You may see a warning that invoices has no records. This is ok for the tutorial. You can type "ignore warning" and continue. 


## Create Destination Connector

To send data from our source, we set up [PGVector](https://supabase.com/docs/guides/database/extensions/pgvector//),  as our destination. This allows for [vector similarity search](https://www.pinecone.io/learn/what-is-similarity-search/),  which will be powerful as shown later. If you are still in the Source Connector builder, tap Exit Builder, then tap Destinations. Type PGVector in the search box and select it from the list, giving it the name "mybot-pgvector" then configure as below:

![pgvector](https://hackmd.io/_uploads/Sk6PJx3B1l.png)

Once we have selected this, we are presented with the following fields which we have to populate: 



![mybot-pgvector](https://hackmd.io/_uploads/rkfAOKRd1g.png)

Under the Processing section, set Chunk size to ``1536``. A chunk is a unit of text, while tokens are how the embedding model measures input size. The Fake embedding model defaults to ``1536`` and that will become important specifically in this tutorial when we implement the RAG logic. 

>[!NOTE]
Make sure that you set the Embedding to Fake. In a production usage you would use something like OpenAI to generate embeddings, but for this tutorial, we will use the [Fake Embedding model from Langchain](https://python.langchain.com/api_reference/core/embeddings/langchain_core.embeddings.fake.FakeEmbeddings.html#fakeembeddings). This will allow us to save cost during the tutorial especially since the [Rate Limits set by OpenAI](https://platform.openai.com/docs/guides/rate-limits#usage-tiers) would get triggered if your account is on the free tier. We will save OpenAI's API for later in the course :)



Under the Indexing section, we will need to add the Supabase host information. To obtain this, from within the Supabase dashboard, tap the Connect button in the top middle, scroll down to Session Pooler, and tap > View Parameter. Here, you will see host string to add to Airbyte. It should look similar to `aws-0-us-west-1.pooler.supabase.com`. For the database,use "postgres,". 

For the Username, take this from the parameters section, right below where the host is. The username will look similar to `postgres.jypjadhnsfgbofupcbjd`. 

For the password, this is the same password you signed up for Supabase with.

![indexing](https://hackmd.io/_uploads/ryGzYF0dJe.png)


## Sync Data

Now that we have our PGVector destination set up, the final step is to configure the connection to tell Airbyte how you want to move data.

Tap Connections from the lefthand menu. Define the source, and select your custom connector, StripeCustomerData



![ssq](https://hackmd.io/_uploads/HJaByghSJl.png)

![seup-destination](https://hackmd.io/_uploads/Bk5I1xhSkx.png)

Next is to test the source with the Stripe API secret key. 

![ss2](https://hackmd.io/_uploads/rkbPJgnrkl.png)


You should see a success message similar to this:

![connection2](https://hackmd.io/_uploads/S17UzuSdyx.png)

After this, select the PGVector destination that you set up earlier by tapping Create a Connection.


![destinationnewwww](https://hackmd.io/_uploads/HJk4Qdruke.png)

Next step is to just wait till the schema is fetched so you can select your streams. 

![destination](https://hackmd.io/_uploads/rk_ufdH_ke.png)


Go ahead and choose the streams created earlier: customers, search customer, invoices, and products. 

![selectstreams](https://hackmd.io/_uploads/B13DXdSO1x.png)


Great! Now, we can configure the connection. 

![configfureconnecTIon](https://hackmd.io/_uploads/HkcQV_Hd1x.png)



Click "Finish & Sync" to finally move the data! 

![airbyteconnectiondone](https://hackmd.io/_uploads/B18HN_Buke.png)

You will know when your sync works when all streams are completed with green checkmarks! 

Before continuing, you will want to make sure that the data was properly moved to Supabase. 

This can be done by logging into the [Supabase dashboard](https://supabase.com/dashboard), and tapping on Table Editor. If there are tables for customers, invoices, and products, you are set! 

To check if your tables exist and have data, tap on SQL Editor and run any of the following queries: 

```sql
SELECT COUNT(*) FROM customers;
```

```sql
SELECT COUNT(*) FROM products;
```

```sql
SELECT COUNT(*) FROM invoices;
```

To test that the emebeddings column has been correctly populated with vector data run a `SELECT` query in SQL editor within Supabase to verify this data being populated. Examples are shown below: 

```sql
-- Check customer embeddings
SELECT id, email, embedding 
FROM customers 
LIMIT 1;
```
```sql
-- Check product embeddings
SELECT id, name, embedding 
FROM products 
LIMIT 1;
```
```sql
-- Check invoice embeddings
SELECT id, customer_id, embedding 
FROM invoices 
LIMIT 1;
```
Each should return a number greater than 0 to indicate data is present within the tables. 


## Recap: Data Movement Pipeline

Congratulations! You've achieved a lot in a short amount of time. You've created a fully functioning data movement pipeline. You've taken data from source such as Stripe and moved it into an AI capable data storage product like Postgres and PGVector. By using Airbyte Cloud, you can quickly schedule when to move data, handle incremental changes in that data, and easily add new data sources ensuring that any AI app you build atop this data pipeline has the most up-to-date and relevant information. Remember, at the heart of AI is access to the right data.


Next, you will create the database functions as the sort of interface for your AI chatbot. 


## Create Database Functions
Duration: ``0:10:00``
At this stage, you should have your Stripe data sync'ed into the public schema running in Supabase. You will have three tables corresponding to the streams you set up in Airbyte. You will also notice that, thanks to the PGVector connector an ``embedding`` column has automatically been created and populated for you. This abtracts the need to create embeddings on our source data and instead, we can focus on creating the context for our LLM to use.

![CleanShot 2024-12-23 at 12.26.28](https://hackmd.io/_uploads/SJjtvSwHyl.png)

In order to utilize those embeddings however, we need to create a few Postgres functions in Supabase. 

These functions will allow us to:

* Query the tables directly from our Python script
* Pass the embeddings of a user's query as an argument
* Perform a similarity search on the source data
* Return data with the closest matches by distance in vectors

Let's go ahead and create each function. From within Supabase, you can head into the SQL Editor tab and copy/paste the SQL below:

>[!NOTE]
>If, when running the queries below, you recieve an error that public.vector cannot be found, first make sure than the PGVector extension is enabled. If it is, replace `public.vector` with `vector`. This will resolve any discrepencies with how your schema is set up. 


### find_related_customer

```sql
CREATE OR REPLACE FUNCTION find_related_customer(question_vector public.vector) 
RETURNS TABLE (
  document_id text,
  chunk_id text,
  metadata json,
  document_content text,
  embedding public.vector
) 
LANGUAGE sql AS $$
    SELECT *
    FROM customers     
    ORDER BY embedding <=> question_vector
    LIMIT 5; 
$$;
```
### find_related_invoices
```sql
CREATE OR REPLACE FUNCTION find_related_invoices(question_vector public.vector) 
RETURNS TABLE (
  document_id text,
  chunk_id text,
  metadata json,
  document_content text,
  embedding public.vector
) 
LANGUAGE sql AS $$
    SELECT *
    FROM invoices  
    ORDER BY embedding <=> question_vector
    LIMIT 5; 
$$;
```

### find_related_products
```sql
CREATE OR REPLACE FUNCTION find_related_products(question_vector public.vector) 
RETURNS TABLE (
  document_id text,
  chunk_id text,
  metadata json,
  document_content text,
  embedding public.vector
) 
LANGUAGE sql AS $$
    SELECT *
    FROM products    
    ORDER BY embedding <=> question_vector
    LIMIT 5; 
$$;
```

At the top of the function, you'll see that an argument called ``question_vector`` is passed into the function as type ``vector``. This is then used in the query to run a similarity search against the embedding column identified by the ``<=>`` operator.

PGVector supports 3 different kinds of operators for computing distance between embeddings:

* ``<->`` Euclidean distance
* ``<#>`` Negative inner product
* ``<=>`` Cosine distance

In this tutorial, we'll be using cosine distance since it's typically a safe option with most embedding models. You can read more on this in [Supabase's docs](https://supabase.com/docs/guides/ai/semantic-search#semantic-search-in-postgres).

With the functions created, we can move on to creating our AI Chatbot!

## The AI Chatbot

Finally, it is time to create the AI chatbot in Python. To make things simple, we will use a Google Collab notebook. You can think of this as an online IDE. Go ahead and navigate to [Google Collab](https://colab.research.google.com/) and create a new notebook called airbyteai. If you would prefer to follow along, here is [a completed notebook](https://colab.research.google.com/drive/1jVFNDFV3JyYWEGj_iTQo0cDjIYzM4aTM) for you.

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



## Summary
Congratulations! You have successfully built your AI chatbot powered by Airbyte. Throughout this course, you learned how to retrieve data from an API source such as Airbyte, and sync with a Vector-enabled data storage such as PGVector. You also learned how embeddings are critical for AI use cases to perform similarity searches in a chatbot. You also used OpenAI's chat completion API to ask natural language questions and retrieve results. 
![aichatnew](https://hackmd.io/_uploads/rJCaQi0O1x.png)

Sit back, give yourself a pat on the shoulder. It's time to put your new found knowledge into practice on your next killer startup! Good luck. 
