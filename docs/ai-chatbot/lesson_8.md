## Sync Data

Now that we have our PGVector destinaiton setup, the final step is to configure the connection to tell Airbyte how you want to move data.

We have to create a new connection, and then define the source, which is going to be the custom Stripe connector built earlier. 



![ssq](https://hackmd.io/_uploads/HJaByghSJl.png)

![seup-destination](https://hackmd.io/_uploads/Bk5I1xhSkx.png)

Next is to test the source with the API key. 

![ss2](https://hackmd.io/_uploads/rkbPJgnrkl.png)


You should see a success message similar to this:

![connection2](https://hackmd.io/_uploads/S17UzuSdyx.png)

After this, you would simply define the destination that you set up earlier, as this will have all the necessary credentials for PGVector. 


![destinationnewwww](https://hackmd.io/_uploads/HJk4Qdruke.png)

Next step is to just wait till the schema is fetched so you can select your streams. 

![destination](https://hackmd.io/_uploads/rk_ufdH_ke.png)


Go ahead and choose the streams created earlier - customers, search customer, invoices, and products. 

![selectstreams](https://hackmd.io/_uploads/B13DXdSO1x.png)


Great! Now, we can configure the connection. 

![configfureconnecTIon](https://hackmd.io/_uploads/HkcQV_Hd1x.png)



Click "Finish & Sync" to finally move the data! 

![airbyteconnectiondone](https://hackmd.io/_uploads/B18HN_Buke.png)

You will know when your sync works when all streams are completed with green checkmarks! 

Ideally, before moving on, you will want to make sure that the data was properly moved to Supabase. 

This can be done by logging into the dashboard, and seeing Table Editor. If there are tables for customers, invoices, and products, you are set! 

There should be an emebeddings column with vector data. 

You can run a `SELECT` query in SQL editor within Supabase to verify this data being populated. Examples are shown below: 

To check if your tables exist and have data - 

```sql
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM invoices;
```

Each should return a number greater than 0 to indicate data. 
To verify embeddings were created, you could run this: 

```sql
-- Check customer embeddings
SELECT id, email, embedding 
FROM customers 
LIMIT 1;

-- Check product embeddings
SELECT id, name, embedding 
FROM products 
LIMIT 1;

-- Check invoice embeddings
SELECT id, customer_id, embedding 
FROM invoices 
LIMIT 1;
```

Note that these are just verification checks to be sure, but there are other ways to check manually too. 

Other than that, you are set! 


