from app.utils.logger import setup_logger
from app.modules.generate import generate_response
from app.modules.ui import build_ui
import gradio as gr

def chatbot_interface(query, chat_history):
    response = generate_response(query)  # 응답 생성
    # 사용자 질문은 유지하고, 새롭게 응답 메시지를 추가
    chat_history.append({"role": "assistant", "content": response})
    return "", chat_history  # 입력창 초기화와 갱신된 기록 반환

# 메인 함수
if __name__ == "__main__":
    # Gradio UI 생성 및 실행
    ui = build_ui(chatbot_interface)
    ui.launch()