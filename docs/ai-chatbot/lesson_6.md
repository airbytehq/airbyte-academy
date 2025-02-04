## Create Source Connector & Streams

Now that we have our database and other environments all set up, we know the source of the data (Stripe) and where we want to move the data, or destination (Postgres on Supabase). It is time to create the data pipeline which will move the data. For this, we will use the Airbyte Cloud platform. To get started, you will need access to your <a href="https://cloud.airbyte.com?utm_medium=lms&utm_source=course-ai" target="_blank">Airbyte credentials</a>, and we will establish our connection first. 

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

If you click on the "Testing Values" button on the top right, you can see where to put your Stripe API key. Using the <a href="https://dashboard.stripe.com/test/apikeys" target="_blank">secret API key</a> in test mode will probably be the best way to do this. 

![stripeapikey](https://hackmd.io/_uploads/SylfWDvSkl.png)

Now that we have the global configuration setup, let's tackle the actual data streams: 

We have four streams in this tutorial that capture the most useful data: 
- Customers
- Search Customer
- Invoices
- Products


### Customers

To set up the Customer Stream, see the <a href="https://docs.stripe.com/api/customers" target="_blank">customers endpoint</a> - /v1/customers. This is of course, our URL path! Click the plus button to get started: 

![customer-stream-setup](https://hackmd.io/_uploads/ByYWfvvryl.png)

We are sending a ``GET`` request and getting JSON as the response. Record selector is selected here which is essential for filtering the records of data. 

![customers](https://hackmd.io/_uploads/SJ5YsFCOke.png)

Tap the test button to ensure everything is working before moving on.

### Search Customer

For the search customer stream, you can use - <a href="https://docs.stripe.com/api/customers/search//" target="_blank">/v1/customers/search </a>as the endpoint. This endpoint takes a query parameter, query and an email in the form of email:"theemail@address.com". If you want to add an email to test, simply tap the Add button beside query parameter using an email created during the Stripe data load. (You an retrieve these by tapping on Customers on the left hand navigation in Stripe) Then, tap Test. 

![search-customer-stream](https://hackmd.io/_uploads/rJTpuTjHkl.png)

### Invoices

Use <a href="https://docs.stripe.com/api/invoices//" target="_blank">/v1/invoices</a> for the endpoint. Toggle "Use an existing stream configuration" on and select Customers. This will copy over configuration for things like the record selector. 

### Products

Use <a href="https://docs.stripe.com/api/products//" target="_blank">/v1/products</a> for the endpoint. Toggle "Use an existing stream configuration" on and select Customers. This will copy over configuration for things like the record selector. 



After building the streams, we can publish the custom connector. Now we just need to build the final connection! Click "Publish" on the top right corner, giving it a name "Stripe-to-Supabase"

![connector-published](https://hackmd.io/_uploads/rywatyhryx.png)

>[!NOTE]
>You may see a warning that invoices has no records. This is ok for the tutorial. You can type "ignore warning" and continue. 


