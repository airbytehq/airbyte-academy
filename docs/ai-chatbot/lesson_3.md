## A Quick AI Terminology Primer

There are a lot of new terms when working with AI. They can be overwhelming, but they don't have to be. Here is a quick primer on the most important things you need to understand. Throughout this tutorial, you will apply many of these techniques in your app. 

1. **RAG** (Retrieval-Augmented Generation) is an AI architecture which can produce accurate and relevant outputs. In this tutorial, RAG will be used to allow the end user to ask questions such as "what are the most popular products sold?". RAG relies on three key technologies: the retrieval system (for this example, embeddings), model (for this example, openAI's LLM), and vector embeddings (for this example, via PGVector)
2. **LLM**: An LLM (Large Language Model) is a type of artificial intelligence model designed to understand and generate human-like text. It is trained on massive datasets of text from diverse sources and uses advanced machine learning techniques to process and generate language. In this tutorial, we will use OpenAI's LLM.
3. **Embeddings**: Embeddings are a type of representation that transforms data (such as text, images, or other inputs) into dense, low-dimensional vectors of numbers. This makes it easier to perform searches against the data, as it is comparing numbers. 
4. **Similarity** **search**: Similarity search is a technique used to find data items that are most similar to a given query item. It is widely applied in tasks where the goal is to retrieve or rank items based on their similarity in content, context, or structure. It is performed against embeddings. 
5. **Hallucinations**: A hallucination refers to a scenario where a generative model, such as a large language model (LLM) that looks correct but factually incorrect, logically flawed, or completely fabricated. The best way to avoid hallucinations is to provide LLMs with domain-specific data. In this case, the data we will provide the LLM will come from Stripe.


![ai-terminology](https://hackmd.io/_uploads/BJKpcworyl.png)


With a primer on key terminology out of the way, it is time to start building your app.

