## Configure Supabase
We are going to use Supabase as the backend and database portion of the chatbot. You should have already completed the pre-requisites and have a Supabase account. If not, <a href="https://supabase.com/dashboard/sign-up" target="_blank">please create one now</a>. 

Once logged in, if you haven't created a Project already, tap *New Project* and select the Organization which you created previously. Name the project, "AirbyteAIBot" and Tap "Create new project".

> [!NOTE]
> If you can not name your project upon initial set up, you can always do it later. Don't worry, the name is not important for any of the code we will write.

Once your project is created, there are a few important things to note, especially when creating Destination connectors from Airbyte, in particular, Project URL and API Key. You will need these shortly. You can always access these keys, via Settings > API (under Configuration) if you need them.

![CleanShot 2024-12-23 at 11.54.55](https://hackmd.io/_uploads/B1VSgBPSJg.png)

Supabase automatically creates a database on your behalf. Tapping on the database icon on the left navigation, and ensuring you have the public schema selected, Supabase currently shows no tables have been created yet. Don't worry, these will be automatically created by Airbyte when you sync data for the first time. 
![CleanShot 2024-12-23 at 12.04.41](https://hackmd.io/_uploads/SJB9zHPr1x.png)

### Enable PGVector Extension
One thing you do need to do is enable PGVector. PGVector is an extension to Postgres to allow it to create and store embeddings. Tap Extensions in the database submenu, and type "PGVector" into the search box, then enable the extension via the toggle. 

![CleanShot 2024-12-23 at 12.07.54](https://hackmd.io/_uploads/r1rI7HwH1e.png)




