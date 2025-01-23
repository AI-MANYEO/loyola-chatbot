import gradio as gr
from app.modules.generate_chroma import generate_response

# Gradio 인터페이스 정의
with gr.Blocks() as demo:
    gr.Markdown("## 📚 도서관 챗봇")
    chatbot_interface = gr.Chatbot(label="도서관 챗봇")  # 채팅 기록을 위한 인터페이스
    user_input = gr.Textbox(label="질문을 입력하세요", placeholder="도서관 관련 질문을 입력하세요...")
    clear_btn = gr.Button("채팅 기록 초기화")  # 초기화 버튼

    chat_history = []

    # Gradio와 기존 generate_response 연결
    def chatbot_handler(user_query, chat_history):
        response = generate_response(user_query)  # generate_response 호출
        chat_history.append((user_query, response))  # 채팅 기록 추가
        return chat_history, chat_history

    # 채팅 기록 초기화 함수
    def clear_chat():
        global chat_history
        chat_history = []
        return "", []

    # Gradio 이벤트 설정
    user_input.submit(chatbot_handler, [user_input, chatbot_interface], [chatbot_interface, chatbot_interface])
    clear_btn.click(clear_chat, [], [chatbot_interface])

# Gradio 앱 실행
if __name__ == "__main__":
    demo.launch(share=True)  # 외부 접속을 허용하려면 share=True 추가
