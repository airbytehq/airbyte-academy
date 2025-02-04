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

This can be done by logging into the <a href="https://supabase.com/dashboard" target="_blank">Supabase dashboard</a>, and tapping on Table Editor. If there are tables for customers, invoices, and products, you are set! 

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


