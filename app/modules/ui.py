import gradio as gr

def build_ui(chatbot_interface):
    with gr.Blocks(css="""
        .send-button {
            background-color: #861F1C;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
        }
        .send-button:hover {
            background-color: #6A1718;
        }
        .clear-button {
            background-color: #808080;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
        }
        .clear-button:hover {
            background-color: #5F5F5F;
        }
        .chat-container {
            height: 2000px; /* 채팅기록 창 높이 */
            overflow-y: scroll; /* 스크롤 유지 */
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 8px;
        }
    """) as interface:
        chat_history = gr.State([])  # 채팅 히스토리 저장

        # 타이틀
        with gr.Row():
            gr.Markdown("## 도서관 챗봇")

        # 채팅 기록
        chatbot = gr.Chatbot(label="채팅 기록", elem_id="chat-container")

        # 입력창과 버튼
        with gr.Row():
            user_input = gr.Textbox(
                placeholder="질문을 입력하세요",
                label="",
                lines=1,
                scale=8
            )
            send_btn = gr.Button("Send", elem_classes="send-button", scale=1)
            clear_btn = gr.Button("Clear", elem_classes="clear-button", scale=1)

        # 버튼 이벤트
        send_btn.click(
            chatbot_interface,
            inputs=[user_input, chat_history],
            outputs=[user_input, chatbot]
        )
        clear_btn.click(
            lambda: (None, []),
            inputs=None,
            outputs=[user_input, chatbot]
        )

    return interface