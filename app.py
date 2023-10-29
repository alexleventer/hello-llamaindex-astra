import os
from pathlib import Path

import cassio
import openai
from dotenv import load_dotenv
from llama_index import StorageContext, VectorStoreIndex
from llama_index.vector_stores import CassandraVectorStore
from llama_index import download_loader


load_dotenv()

ASTRA_DB_ID = os.environ["ASTRA_DB_ID"]
ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

cassio.init(
    database_id=ASTRA_DB_ID,
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace=ASTRA_DB_KEYSPACE,
)

cassandra_store = CassandraVectorStore(table="nasa", embedding_dimension=1536)

PDFReader = download_loader("PDFReader")

loader = PDFReader()
documents = loader.load_data(file=Path('./documents/nasa-rockets-guide.pdf'))

storage_context = StorageContext.from_defaults(vector_store=cassandra_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)


def query_store(question):
    query_engine = index.as_query_engine()
    return query_engine.query(question)


if __name__ == '__main__':
    answer = query_store('What sort of experiments did Galileo conduct?')
    print(answer.response)
