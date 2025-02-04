## Pre-requisites

To get started, you will need to set up the following accounts. Lucky for you - you can complete this entire course using free or trial versions. You will not require a credit card or paid account. 

1. Stripe: Stripe is a very popular platform for processing online payments, with great developer APIs. You will need to <a href="https://dashboard.stripe.com/register" target="_blank">Sign up</a> for Stripe account. This will allow you to access test Stripe data for users, products, invoices, and purchases. You do not need to add any payments information. You can skip this during the setup.
2. Airbyte Cloud: Airbyte will be used as the data movement platform connecting Stripe with a modern database like Postgres to enable RAG applications. You will use a 14-day trial of Airbyte Cloud. You can <a href="https://cloud.airbyte.com/signup?utm_medium=lms&utm_source=course-ai" target="_blank">sign up here</a>. If you already have an Airbyte Cloud account, please feel free to use this. 
3. Supabase: Supabase is a cloud-based backend-as-a service. At it's core, it is a managed PostgresSQL database. We will use this database, with the PGVector extension to build a RAG application. <a href="https://supabase.com/dashboard/sign-in" target="_blank">Sign up here</a> and create an empty project, giving it whatever name you like. Make sure you write down the database password. You will need later.
4. OpenAI: OpenAI, the makers of ChatGPT provide an API platform for developers to build solutions with natural language processing and similarity search. <a href="https://platform.openai.com/" target="_blank">Sign up for a free account.</a> You will use this for your chatbot to perform searches on your data using the <a href="https://platform.openai.com/docs/api-reference/chat" target="_blank">Chat Completion API</a>.   
5. Google Account: You will create the chatbot code in Python using a Google Collab notebook. In order to do so, you will need a <a href="https://accounts.google.com/lifecycle/steps/signup/name" target="_blank">free gmail account</a>. If you prefer to code locally, in your favorite IDE instead of a collab notebook, please do so, just keep in mind, this tutorial will not cover local Python environment configuration. 

Once you have created all of your accounts. Let's continue.



