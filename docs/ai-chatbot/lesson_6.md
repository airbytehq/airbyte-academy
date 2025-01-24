## Create Source Connector & Streams

At this point, we have know the source of the data (stripe) and where we want to move the data, or destination (postgres on supabase). It is time to move the data. For this, we will use the Airbyte Cloud platform. To get started, you will need access to your [Airbyte credentials](https://cloud.airbyte.com/signup?utm_campaign=TDD_Search_Brand_USA&utm_source=adwords&utm_term=airbyte%20cloud&_gl=1*v7yfqs*_gcl_aw*R0NMLjE3MzQ5ODcwNDAuQ2owS0NRaUFzYVM3QmhEUEFSSXNBQVg1Y1NBOEFiMXd5RE45YzNOVFRRYU04ODNHdU5VRDBwV2RyUXlrYWp0OWI0WGJrMVNSQnRpUGpOa2FBakdrRUFMd193Y0I.*_gcl_au*OTc3Mjg2MDc0LjE3MzA4NDY2MjIuNDg2MzQ0NDM3LjE3MzIwNTI0ODAuMTczMjA1MjQ3OQ..//), and we will establish our connection first. 

Within Airbyte, tap Builder in the left menu, then New custom Connection.

![airbytecircles](https://hackmd.io/_uploads/SJvp6IDrJl.png)

You will be presented with options to create your connector. Select Start from Scratch. 

We're starting from scratch to have complete control over our API configuration and to precisely define what Stripe data we want to include in our AI pipeline.



![startfromscratch ](https://hackmd.io/_uploads/SJrdn8PBJg.png)

:::info
Airbyte offers a pre-built Stripe connector. We could have used this in the tutorial, but wanted to get you hands-on with the connector builder, and it allows us more control over specific fields that we want to sync.
:::

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

We are sending a GET request and getting JSON as the response. Record selector is selected here which is essential for filtering the records of data. 

![customerstream](https://hackmd.io/_uploads/rkc3MmsHkx.png)

### Search Customer

For the search customer stream, you can use - [/v1/customers/search ](https://docs.stripe.com/api/customers/search//)as the endpoint. On the right, you can see the response if you filter query by specific email.  

![search-customer-stream](https://hackmd.io/_uploads/rJTpuTjHkl.png)

### Invoices

Use [/v1/invoices](https://docs.stripe.com/api/invoices//) for the endpoint. 

### Products

Use [/v1/products](https://docs.stripe.com/api/products//) for the endpoint. 

Note that invoices and products are set up the same way, but you can choose to add whatever field path is best and pagination if needed. 

After building the streams, we can publish the custom connector. Now we just need to build the final connection! Click "Publish" on the top right corner. 

![connector-published](https://hackmd.io/_uploads/rywatyhryx.png)


