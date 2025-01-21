import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from app.modules.generate import generate_answer
from app.utils.logger import setup_logger

logger=setup_logger(name="search")
# Load the Sentence Transformer model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

'''
사용자 질문과 csv 데이터 유사도 분석
'''
def find_similar_question(data, query, column_name="서명", top_n=5, threshold=0.8):
    questions = data[column_name].fillna("").tolist()
    question_embeddings = model.encode(questions, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, question_embeddings)

    top_results = torch.topk(similarities, k=top_n)
    indices = top_results.indices[0].cpu().numpy()
    scores = top_results.values[0].cpu().numpy()

    results = [
        {"서명": questions[i], "Score": scores[idx]}
        for idx, i in enumerate(indices) if scores[idx] > threshold
    ]
    return results


def get_answer(data, query):
    """
    Retrieves a generated answer using OpenAI API based on the user's query and the most similar book title.
    """
    similar_questions = find_similar_question(data, query, column_name="서명", top_n=5)

    if not similar_questions:
        print("[DEBUG] 관련 데이터를 찾을 수 없음. 신착자료 추천 기능 사용")
        return recommend_books(data, query)

    # 가장 유사한 서명 및 해당 도서 정보 가져오기
    best_match = similar_questions[0]
    relevant_answer = data.loc[data["서명"] == best_match["서명"], ["소장처","저자","출판사","발행년","자료유형"]]

    # **[디버깅 출력] 챗봇이 사용한 데이터 표시**
    print(f"\n[DEBUG] 유사 서명 선택: {best_match['서명']} (유사도 점수: {best_match['Score']:.2f})")
    print(f"[DEBUG] 검색된 도서 정보: \n{relevant_answer}\n")

    if not relevant_answer.empty:
        return generate_answer(query, best_match["서명"], relevant_answer.values[0])
    else:
        print("[DEBUG] 관련 도서 정보가 없음 → 신착자료 추천 기능 사용")
        return recommend_books(data, query)
