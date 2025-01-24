## Pre-requisites

To get started, you will need to set up the following accounts. Lucky for you - you can complete this entire course using free or trial versions. You will not require a credit card or paid account. 

1. Stripe: Stripe is a very popular platform for processing online payments, with great developer APIs. You will need to [Sign up](https://dashboard.stripe.com/register) for Stripe account. This will allow you to access test Stripe data for users, products, invoices, and purchases. You do not need to add any payments information. You can skip this during the setup.
2. Airbyte Cloud: Airbyte will be used as the data movement platform connecting Stripe with a modern database like Postgres to enable RAG applications. You will use a 14-day trial of Airbyte Cloud. You can [sign up here](https://cloud.airbyte.com/signup?utm_medium=lms&utm_source=course-ai). If you already have an Airbyte Cloud account, please feel free to use this. 
3. Supabase: Supabase is a cloud-based backend-as-a service. At it's core, it is a managed PostgresSQL database. We will use this database, with the PGVector extension to build a RAG application. [Sign up here] (https://supabase.com/dashboard/sign-in) and create an empty project, giving it whatever name you like. 
4. OpenAI: OpenAI, the makers of chatGPT provide an API platform for developers to build solutions with natural language processing and similarity search. [Sign up for a free account.](https://auth.openai.com/authorize) You will use this for your chatbot to perform searches on your data.  
5. Google Account: You will create the chatbot code in Python using a Google Collab notebook. In order to do so, you will need a [free gmail account](https://accounts.google.com/lifecycle/steps/signup/name). If you prefer to code locally, in your favorite IDE instead of a collab notebook, please do so, just keep in mind, this tutorial will not cover local Python environment configuration. 

Once you have created all of your accounts. Let's continue.



