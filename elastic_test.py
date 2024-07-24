import os
from elasticsearch import Elasticsearch

username = 'elastic'
password = os.getenv('ELASTIC_PASSWORD') # Value you set in the environment variable

client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(username, password)
)

print(client.info())