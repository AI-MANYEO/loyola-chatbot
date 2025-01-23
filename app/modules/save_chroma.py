import json
import os
import chromadb
from database.chroma_manager import *

def load_data_to_chromadb():
    data_folder = "database/raw/"
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(data_folder, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        for entry in data:
            title = entry.get("title", "제목 없음")
            url = entry.get("url", "")
            category = entry.get("category", "")
            subcategory = entry.get("subcategory", "")
            description = entry.get("description", [])
            
            # description 내 content 값들을 텍스트로 변환
            texts = []
            for desc in description:
                if isinstance(desc, dict) and "content" in desc:
                    content = desc["content"]
                    if isinstance(content, dict):
                        texts.extend([str(v) for v in content.values()])
                    elif isinstance(content, list):
                        texts.extend([str(item) for item in content])
                    else:
                        texts.append(str(content))
            
            combined_text = " ".join(texts)
            if not combined_text.strip():
                continue  # 빈 설명은 저장하지 않음
            
            vector = embedding_model.encode(combined_text).tolist()
            
            doc_id = f"{title}-{url}"  # 고유 ID 생성
            
            collection.add(
                ids=[doc_id],
                embeddings=[vector],
                metadatas=[{
                    "title": title,
                    "url": url,
                    "category": category,
                    "subcategory": subcategory,
                    "content": combined_text
                }]
            )
        
    print("모든 데이터를 크로마DB에 저장 완료!")

if __name__ == "__main__":
    load_data_to_chromadb()
