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

In this tutorial, we'll be using cosine distance since it's typically a safe option with most embedding models. You can read more on this in <a href="https://supabase.com/docs/guides/ai/semantic-search#semantic-search-in-postgres" target="_blank">Supabase's docs</a>.

With the functions created, we can move on to creating our AI Chatbot!

