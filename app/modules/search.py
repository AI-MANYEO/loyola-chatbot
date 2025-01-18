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
def find_similar_question(data, query, column_name="Question", top_n=1):
    """
    Finds the most similar questions in the dataset based on the query.
    """
    # Extract the questions from the dataset
    questions = data[column_name].fillna("").tolist()

    # Encode the questions and the query
    question_embeddings = model.encode(questions, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(query_embedding, question_embeddings)

    # Get the top N most similar questions
    top_results = torch.topk(similarities, k=top_n)
    indices = top_results.indices[0].cpu().numpy()
    scores = top_results.values[0].cpu().numpy()

    # Return the results as a list of dictionaries
    
    # results = [{"Question": questions[i], "Score": scores[idx]} for idx, i in enumerate(indices)]
    results = [{"서명": questions[i], "Score": scores[idx]} for idx, i in enumerate(indices)]
    return results

def get_answer(data, query):
    """
    Retrieves a generated answer using OpenAI API based on the user's query and the most similar FAQ.
    """
    # Find the most similar question
    # similar_questions = find_similar_question(data, query, column_name="Question", top_n=1)
    similar_questions = find_similar_question(data, query, column_name="서명", top_n=1)

    if similar_questions:
        # Get the most similar question and its corresponding answer
        best_match = similar_questions[0]
        #relevant_answer = data.loc[data["Question"] == best_match["Question"], "Answer"].values
        relevant_answer = data.loc[data["서명"] == best_match["서명"], ["소장처","저자","출판사","발행년","자료유형"]].values

        if len(relevant_answer) > 0:
            # Use OpenAI API to generate a more detailed answer
            # return generate_answer(query, best_match["Question"], relevant_answer[0])
            return generate_answer(query, best_match["서명"], relevant_answer[0])
        else:
            return "관련 데이터를 찾을 수 없습니다."
    else:
        return "관련 데이터를 찾을 수 없습니다."
