## Intro

Users can interact with the Airbyte platform outside of the UI using an API.

This enables developers to integrate Airbyte into their monitoring system, data pipeline, or own product.

The easiest way to interact with an API, when the provider offers this option, is through their API website. Airbyte provides the ability to run API calls directly on their <a href="https://reference.airbyte.com/reference/getting-started" target="_blank">website</a>. This eliminates the need for external tools to test your credentials. Other tools, such as Postman or the curl command in the terminal, also simplify this process. These methods are typically used to test commands and credentials. However, the most common approach for developers is to integrate the API using a software development kit (SDK).

Airbyte provide two SDK:
- <a href="https://github.com/airbytehq/airbyte-api-python-sdk" target="_blank">Airbyte API Python SDK</a>
- <a href="https://github.com/airbytehq/airbyte-api-java-sdk" target="_blank">Airbyte API Java SDK</a>

In this course, we will build a simple yet functional data pipeline. We will create a source (Faker Sample) and a destination (MotherduckDb), establish the connection between them, and trigger the sync to ingest data into the destination.

