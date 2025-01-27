import chromadb
from database.chroma_manager import *

def search_library(query, top_k=5):
    """사용자의 질문(query)에 대해 크로마DB에서 유사한 데이터를 검색"""
    collection = client.get_or_create_collection(name="library_collection")

    query_vector = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas"]  # ✅ 검색 결과에 documents 포함
    )

    # ✅ `metadatas`만 반환 (documents는 사용하지 않으므로 제외 가능)
    return results["metadatas"] if results["metadatas"] else []


# if __name__ == "__main__":
#     query = input("질문을 입력하세요: ")
#     result = search_library(query)
#     print("검색된 데이터:", result)
