## Create Database Functions

At this stage, you should have your Stripe data sync'ed into the public schema running in Supabase. You will have three tables corresponding to the streams you set up in Airbyte. You will also notice that, thanks to the PGVector connector an embeddings column has automatically been created and populated for you. We are going to use this to perform a similarity search via openAI and your chatbot.

![CleanShot 2024-12-23 at 12.26.28](https://hackmd.io/_uploads/SJjtvSwHyl.png)

Before we do however, we need to create a few helper functions. These functions, one for each table, will pass in a question vector from openAI and compare this to the embedding of each record to find matches. Put simply, openAI takes a natural language question, converts it to a vector or numerical value, then we want to compare this to the numerical value of the embedding. The closer these two numbers are, the more relevant the results are. 

Let's go ahead and create each function. From within Supabase, make sure you are in the database section, then tap Functions, Create new function. Repeat this process to create the following three functions. Each function takes a single argument, question_vector, of return type vector.

:::info

For this section, you will have to use PLpgSQL in the function definition, which is essentially just an extension on top of normal SQL. This may cause syntax errors so we reccomend using SQL editor to test in, as your playground! 

:::
### find_related_customer

```sql
SELECT *
    FROM customers     
    ORDER BY embedding <=> question_vector;
```

### find_related_invoices
```sql
SELECT *
    FROM invoices     
    ORDER BY embedding <=> question_vector
```

### find_related_products

```sql
    SELECT *
    FROM products     
    ORDER BY embedding <=> question_vector
```
That's it. Make sure all of your work is saved, and your Airbyte Sync is complete and populated data. Now it's time to create the chatbot. 

![Screenshot 2025-01-07 at 12.02.20 PM](https://hackmd.io/_uploads/BJYIubiIye.png)

