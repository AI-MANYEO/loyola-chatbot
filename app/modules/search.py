import chromadb
from database.chroma_manager import *

def search_library(query, top_k=5):
    """사용자의 질문(query)에 대해 크로마DB에서 유사한 데이터를 검색하여 반환"""
    
    query_vector = embedding_model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas"]  # ✅ 검색 결과에 documents 포함
    )

    filtered_results = []
    
    # 🔹 "metadatas"가 2중 리스트일 경우 flatten 처리
    metadatas = results.get("metadatas", [])
    if len(metadatas) > 0 and isinstance(metadatas[0], list):
        metadatas = [item for sublist in metadatas for item in sublist]  # 🔹 리스트 평탄화 (flatten)

    documents = results.get("documents", [])  # 🔹 기본값을 빈 리스트로 설정

    for i, metadata in enumerate(metadatas):
        # ✅ documents가 존재하는지 확인 후 가져오기
        document = documents[i] if i < len(documents) else "정보 없음"

        # ✅ documents가 리스트일 경우 첫 번째 요소 선택
        if isinstance(document, list) and len(document) > 0:
            document = document[0]  # 🔹 리스트의 첫 번째 요소 가져오기

        # ✅ JSON 문자열이면 변환
        if isinstance(document, str) and document.startswith("{"):
            try:
                document = json.loads(document)  # 🔹 JSON 문자열을 딕셔너리로 변환
            except json.JSONDecodeError:
                pass  # 🔹 JSON 파싱 실패 시 그냥 문자열 유지

        if isinstance(metadata, dict):
            filtered_results.append({
                "title": metadata.get("title", "제목 없음"),
                "category": metadata.get("category", "카테고리 없음"),
                "subcategory": metadata.get("subcategory", "서브카테고리 없음"),
                "description": document  # ✅ 수정된 description 처리
            })

    return filtered_results[:top_k]
