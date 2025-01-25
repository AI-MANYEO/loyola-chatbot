import json
import os
import chromadb
from database.chroma_manager import *

def load_data_to_chromadb():
    data_folder = "database/raw/"

    for file_name in os.listdir(data_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(data_folder, file_name)
            
            print(f"📂 로드 중: {file_name}")  # JSON 파일 로드 시작 로그

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)  # JSON 파일 로드
                    print(f"✅ {file_name} 로드 완료 (항목 개수: {len(data)})")  # 데이터 개수 출력
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON 파일 {file_name} 로드 실패: {e}")
                    continue  # JSON 파싱 실패하면 다음 파일로 넘어감
                
            if not isinstance(data, list):
                print(f"⚠️ {file_name}의 JSON 데이터가 리스트 형태가 아닙니다. 건너뜁니다.")
                continue  # JSON 파일이 리스트가 아닐 경우 스킵

            for idx, entry in enumerate(data):
                title = entry.get("title", "제목 없음")
                tab = entry.get("tab", "")  # tab 필드 추가
                url = entry.get("url", "")
                category = entry.get("category", "")
                subcategory = entry.get("subcategory", "")
                description = entry.get("description", [])

                # description이 리스트라면 모든 요소를 문자열로 변환 후 합치기
                if isinstance(description, list):
                    combined_text = " ".join(map(str, description))
                else:
                    combined_text = str(description)  # 리스트가 아니면 문자열로 변환

                # 빈 값이어도 디비에 저장
                vector = embedding_model.encode(combined_text).tolist()
                
                doc_id = f"{title}-{url}"  # 고유 ID 생성
                
                collection.add(
                    ids=[doc_id],
                    embeddings=[vector],
                    metadatas=[{
                        "title": title,
                        "tab": tab,  # tab 추가
                        "url": url,
                        "category": category,
                        "subcategory": subcategory,
                        "content": combined_text  # 빈 값이어도 저장
                    }]
                )
                
                print(f"📝 저장 완료: {title} (Tab: {tab}, URL: {url})")  # 데이터 저장 로그

    print("✅ 모든 데이터를 크로마DB에 저장 완료!")

if __name__ == "__main__":
    load_data_to_chromadb()
