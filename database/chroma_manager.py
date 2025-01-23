import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
load_dotenv()

# EC2 퍼블릭 IP와 ChromaDB 포트
HOST = os.environ.get("CHROMADB_HOST")
PORT = os.environ.get("CHROMADB_PORT")


client = chromadb.HttpClient(host=HOST, port=PORT)
collection = client.get_or_create_collection(name="library_collection")
collections = client.list_collections()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("현재 존재하는 컬렉션 목록:")
for collection_name in collections:
    print(collection_name)