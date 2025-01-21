import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

# EC2 퍼블릭 IP와 ChromaDB 포트
HOST = os.environ.get("CHROMADB_HOST")
PORT = os.environ.get("CHROMADB_PORT")


client = chromadb.HttpClient(host=HOST, port=PORT)
collections = client.list_collections()

print("현재 존재하는 컬렉션 목록:")
for collection_name in collections:
    print(collection_name)