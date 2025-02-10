import json
import os
import chromadb
import numpy as np
from database.chroma_manager import *

def reset_chromadb():
    """크로마DB 컬렉션 초기화"""
    global collection
    print("🚀 크로마DB 컬렉션 초기화 중...")

    # 기존 컬렉션 삭제 후 새로 생성
    client.delete_collection(name="library_collection")
    collection = client.get_or_create_collection(name="library_collection")

    print("✅ 크로마DB 초기화 완료!")

def format_description(description):
    """description이 리스트인 경우 문자열로 반환"""
    if isinstance(description, list):
        formatted = []
        for item in description:
            if isinstance(item, dict):
                # 딕셔너리 데이터를 JSON 문자열로 변환
                formatted.append(json.dumps(item, ensure_ascii=False))
            else:
                formatted.append(str(item))
        return " ".join(formatted)
    return str(description)



def load_data_to_chromadb():
    data_folder = "database/raw/"

    for file_name in os.listdir(data_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(data_folder, file_name)
            
            print(f"📂 로드 중: {file_name}")

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    print(f"✅ {file_name} 로드 완료 (항목 개수: {len(data)})")
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON 파일 {file_name} 로드 실패: {e}")
                    continue
                
            if not isinstance(data, list):
                print(f"⚠️ {file_name}의 JSON 데이터가 리스트 형태가 아닙니다. 건너뜁니다.")
                continue

            for idx, entry in enumerate(data):
                title = entry.get("title", "제목 없음")
                tab = entry.get("tab", "")
                url = entry.get("url", "")
                category = entry.get("category", "")
                subcategory = entry.get("subcategory", "")
                description = format_description(entry.get("description", []))

                # 🔹 벡터 임베딩 생성 (예외 처리 포함)
                try:
                    vector = np.array(embedding_model.encode(description)).tolist()  # ✅ `numpy.array` 변환
                    print(f"✅ 벡터 생성 완료: {title} (벡터 길이: {len(vector)})")
                except Exception as e:
                    print(f"⚠️ 벡터 임베딩 오류: {title}, 오류: {e}")
                    continue

                doc_id = f"{title}-{url}"

                # ✅ 데이터를 `add()`에서 한 번에 저장 (벡터 포함)
                collection.add(
                    ids=[doc_id],
                    embeddings=[vector],  # ✅ 벡터 포함
                    documents=[description],
                    metadatas=[{
                        "title": title,
                        "tab": tab,
                        "url": url,
                        "category": category,
                        "subcategory": subcategory
                    }]
                )

                print(f"📝 저장 완료: {title} (Tab: {tab}, URL: {url})")

    print("✅ 모든 데이터를 크로마DB에 저장 완료!")

    """
    # ✅ 수정: embeddings 포함 여부 확인
    stored_data = collection.get(include=["embeddings", "metadatas", "documents"])
    
    if len(stored_data["embeddings"]) == 0:  # ✅ 올바른 방식으로 수정
        print("❌ 크로마DB에 벡터 데이터가 저장되지 않았습니다!")
    else:
        print(f"✅ 크로마DB에 저장된 벡터 개수: {len(stored_data['embeddings'])}")
    """

if __name__ == "__main__":
    reset_chromadb()  # 기존 데이터 초기화
    load_data_to_chromadb()  # 새 데이터 저장
