## Create Destination Connector

To send data from our source, we set up <a href="https://supabase.com/docs/guides/database/extensions/pgvector//" target="_blank">PGVector</a>,  as our destination. This allows for <a href="https://www.pinecone.io/learn/what-is-similarity-search/" target="_blank">vector similarity search</a>,  which will be powerful as shown later. If you are still in the Source Connector builder, tap Exit Builder, then tap Destinations. Type PGVector in the search box and select it from the list, giving it the name "mybot-pgvector" then configure as below:

![pgvector](https://hackmd.io/_uploads/Sk6PJx3B1l.png)

Once we have selected this, we are presented with the following fields which we have to populate: 



![mybot-pgvector](https://hackmd.io/_uploads/rkfAOKRd1g.png)

Under the Processing section, set Chunk size to ``1536``. A chunk is a unit of text, while tokens are how the embedding model measures input size. The Fake embedding model defaults to ``1536`` and that will become important specifically in this tutorial when we implement the RAG logic. 

>[!NOTE]
Make sure that you set the Embedding to Fake. In a production usage you would use something like OpenAI to generate embeddings, but for this tutorial, we will use the <a href="https://python.langchain.com/api_reference/core/embeddings/langchain_core.embeddings.fake.FakeEmbeddings.html#fakeembeddings" target="_blank">Fake Embedding model from Langchain</a>. This will allow us to save cost during the tutorial especially since the <a href="https://platform.openai.com/docs/guides/rate-limits#usage-tiers" target="_blank">Rate Limits set by OpenAI</a> would get triggered if your account is on the free tier. We will save OpenAI's API for later in the course :)



Under the Indexing section, we will need to add the Supabase host information. To obtain this, from within the Supabase dashboard, tap the Connect button in the top middle, scroll down to Session Pooler, and tap > View Parameter. Here, you will see host string to add to Airbyte. It should look similar to `aws-0-us-west-1.pooler.supabase.com`. For the database,use "postgres,". 

For the Username, take this from the parameters section, right below where the host is. The username will look similar to `postgres.jypjadhnsfgbofupcbjd`. 

For the password, this is the same password you signed up for Supabase with.

![indexing](https://hackmd.io/_uploads/ryGzYF0dJe.png)


