import chromadb
from database.chroma_manager import *


def search_library(query, top_k=3):
    """사용자의 질문(query)에 대해 크로마DB에서 유사한 데이터를 검색하여 반환"""
    query_vector = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    if results["metadatas"]:
        return results["metadatas"][0]  # 가장 유사한 문서 반환
    else:
        return None

# if __name__ == "__main__":
#     query = input("질문을 입력하세요: ")
#     result = search_library(query)
#     print("검색된 데이터:", result)
