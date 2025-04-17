## Introduction

PyAirbyte wraps the entire Airbyte connector catalogue in a friendly Python API. Instead of running the Airbyte platform you can pull data right inside a Jupyter/Colab notebook, a scheduled script, or a production service. In this course we will:

* Install and configure PyAirbyte.
* Build a pipeline that pulls data from Stripe into DuckDB.
* Persist data in MotherDuck and keep it incrementally updated.
* Run a custom manifest‑only connector built with the Airbyte Connector Builder.
* Load data into a vector database and run semantic queries (RAG).

Along the way we will cover secret management, caching options, and deployment tips.

###  Prerequisites

| Skill / Tool            | Minimum level                           |
| ----------------------- | --------------------------------------- |
| Python                  | Basic syntax & packages                 |
| GitHub or Google Colab  | Able to run notebooks                   |
| MotherDuck account      | Free tier is fine                       |

> [!Tip]
> All examples run in Colab so you can follow even on an iPad.


