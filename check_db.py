import chromadb
import pandas as pd
import numpy as np
from database.chroma_manager import *

# 크로마DB 클라이언트 연결 (EC2 서버)
client = chromadb.HttpClient(host=HOST, port=PORT)
collection = client.get_collection(name="library_collection")

def check_chromadb():
    """크로마DB에 저장된 모든 데이터를 확인"""
    stored_data = collection.get(include=["embeddings", "metadatas", "documents"])
    
    # ✅ 저장된 데이터 개수 확인
    print(f"📌 크로마DB 저장된 데이터 개수: {len(stored_data['ids'])}")
    
    # ✅ 각 필드의 길이 출력
    print("📌 각 필드 길이 확인:")
    for key, value in stored_data.items():
        if value is not None:
            print(f" - {key}: {len(value)}")
        else:
            print(f" - {key}: ❌ None 값입니다.")

    # ✅ 저장된 메타데이터 확인 (상위 5개 출력)
    if stored_data["metadatas"]:
        print("\n📌 저장된 메타데이터 예시 (상위 5개):")
        df = pd.DataFrame(stored_data["metadatas"][:])
        print(df)
    
    # ✅ 저장된 문서 내용 확인 (상위 5개 출력)
    if stored_data["documents"]:
        print("\n📌 저장된 문서 예시 (상위 5개):")
        for i, doc in enumerate(stored_data["documents"][:]):
            print(f"{i+1}. {doc[:100]}...")  # 문서 내용 앞부분만 출력

    # ✅ 저장된 벡터 크기 확인
    if isinstance(stored_data["embeddings"], list) and len(stored_data["embeddings"]) > 0:
        print("\n📌 저장된 벡터 개수:", len(stored_data["embeddings"]))
        print("📌 임베딩 벡터 샘플:", np.array(stored_data["embeddings"][:1]))  # 첫 번째 벡터 샘플 출력

if __name__ == "__main__":
    check_chromadb()
