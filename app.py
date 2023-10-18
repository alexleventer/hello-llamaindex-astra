import os

import openai
from pathlib import Path
from dotenv import load_dotenv
from llama_index import (VectorStoreIndex, StorageContext, )
from llama_index.vector_stores import CassandraVectorStore
from llama_index import download_loader
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

load_dotenv()

ASTRA_DB_TOKEN = os.getenv("ASTRA_DB_TOKEN")
ASTRA_DB_SCB = os.getenv("ASTRA_DB_SCB")
ASTRA_KEYSPACE = os.getenv("ASTRA_KEYSPACE")
openai.api_key = os.getenv("OPENAI_API_KEY")

cluster = Cluster(cloud={"secure_connect_bundle": ASTRA_DB_SCB},
                  auth_provider=PlainTextAuthProvider("token", ASTRA_DB_TOKEN, ), )
session = cluster.connect()

cassandra_store = CassandraVectorStore(session=session, keyspace=ASTRA_KEYSPACE, table="nasa",
    embedding_dimension=1536, )

PDFReader = download_loader("PDFReader")

loader = PDFReader()
documents = loader.load_data(file=Path('./documents/nasa-rockets-guide.pdf'))

storage_context = StorageContext.from_defaults(vector_store=cassandra_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)


def query_store(question):
    query_engine = index.as_query_engine()
    return query_engine.query(question)


if __name__ == '__main__':
    response = query_store('What sort of experiments did Galileo conduct?')
    print(response)
