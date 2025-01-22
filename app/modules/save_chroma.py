import json
import os
import chromadb
from database.chroma_manager import *

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# data_folder = os.path.join(BASE_DIR, "/database/raw")



def load_data_to_chromadb():
    data_folder = "database/raw/"

    for file_name in os.listdir(data_folder):
        if file_name.endswith(".json"):  
            file_path = os.path.join(data_folder, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # JSON 구조에 따라 title과 content 설정
            title = data.get("메뉴", "제목 없음")
            texts = " ".join(data["내용"].get("texts", []))  # 모든 텍스트를 하나로 합침

            vector = embedding_model.encode(texts).tolist()

            
            collection.add(
                ids=[file_name],  # 파일명을 ID로 
                embeddings=[vector],
                metadatas=[{"title": title, "content": texts}]
            )

    print("모든 JSON 파일을 크로마DB에 저장 완료!")
