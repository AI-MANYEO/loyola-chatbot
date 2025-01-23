import json
import os
import chromadb
from database.chroma_manager import *

def load_data_to_chromadb():
    data_file = "database/raw/sogang_library_structured.json"

    with open(data_file, "r", encoding="utf-8") as f:
        data_list = json.load(f)  # JSON이 리스트 구조이므로 직접 리스트 로드

    for page_data in data_list:
        url = page_data.get("url", "No URL")
        title = page_data.get("title", "No Title")
        category = page_data.get("category", "No Category")
        subcategory = page_data.get("subcategory", "No Subcategory")
        
        # description에서 section과 content를 합쳐 하나의 텍스트로 변환
        description_texts = []
        for section in page_data.get("description", []):
            section_title = section.get("section", "")
            section_content = " ".join([str(item) for item in section.get("content", [])])
            description_texts.append(f"{section_title}: {section_content}")

        full_text = f"{title} {category} {subcategory} " + " ".join(description_texts)

        # 벡터 임베딩 생성
        vector = embedding_model.encode(full_text).tolist()

        # ChromaDB에 추가
        collection.add(
            ids=[url],  # URL을 ID로 사용
            embeddings=[vector],
            metadatas=[{
                "title": title,
                "category": category,
                "subcategory": subcategory,
                "content": full_text
            }]
        )

    print("모든 JSON 데이터를 크로마DB에 저장 완료!")

