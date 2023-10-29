# Hello Llama Index Astra
A simple app demonstrating the Llama Index/Astra Integration.

## Getting Started

1. Create a `.env` file based on the `.env` example (see below)
2. Install the dependencies with e.g. `pip install -r requirements.txt`. _(Python 3.8+ required. Working in a virtual environment is suggested as general best practice)_.
3. Run the app with `python app.py` !

### The dot-env file

The environment variables expected in the `.env` file are:

- `OPENAI_API_KEY`, your OpenAI API key.
- `ASTRA_DB_APPLICATION_TOKEN`, the Token to access your Astra DB instance. The token must be created with role "Database Administrator".
- `ASTRA_DB_ID`, the ID of your Astra DB, which you can find at the top of your dashboard in the Astra UI.
= `ASTRA_DB_KEYSPACE` **(optional)**, the name of your keyspace in the database. If omitted, the app will default to using the main keyspace originally created with the DB.
