## Create Destination Connector

To send data from our source, we set up <a href="https://supabase.com/docs/guides/database/extensions/pgvector//" target="_blank">PGVector</a>,  as our destination. This allows for vector similarity search,  which will be powerful as shown later.

![pgvector](https://hackmd.io/_uploads/Sk6PJx3B1l.png)

Once we have selected this, we are presented with the following fields which we have to populate: 




![pgvectordes-new](https://hackmd.io/_uploads/Skg_nwBu1x.png)

Note that for destination settings, we must set up the indexing by choosing OpenAI, inserting the respective API key, and choosing the "text-embedding-ada-002" model.

Supabase host should just be something like aws-0-us-west-1.pooler.supabase.com, while the database is "postgres," followed by your respective Supabase user and password credentials. 

