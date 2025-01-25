import gradio as gr

def build_ui(chatbot_interface):
    with gr.Blocks(css="""
    /* 서강체 폰트 로드 */
        @font-face {
            font-family: 'Sogang';
            src: url('/static/fonts/SOGANG_UNIVERSITY_for_windows.ttf') format('truetype'); 
        }

        .send-button, .clear-button {
            padding: 12px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: transform 0.2s, background-color 0.2s;
        }
        .send-button {
            background-color: #861F1C;
            color: white;
        }
        .send-button:hover {
            background-color: #6A1718;
            transform: scale(1.05);
        }
        .clear-button {
            background-color: #808080;
            color: white;
        }
        .clear-button:hover {
            background-color: #5F5F5F;
            transform: scale(1.05);
        }
        .chat-container {
            height: 500px;  /* Increased height */
            overflow-y: auto;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: #333;
        }
        .bot-message {
            background-color: #9C2A2A;  /* 서강대색*/
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        .user-message {
            background-color: #d3d3d3;
            border-radius: 10px;
            padding: 10px;
            color: black;
        }
        .header-title {
            display: flex;
            align-items: center;
            font-family: 'Sogang', sans-serif; /* 서강체 폰트 적용 */
            font-size: 36px;  /* 글씨 크기 증가 */
            font-weight: bold; /* 굵게 */
        }
        .header-title img {
            width: 50px;  /* Adjust icon size */
            height: auto;
            margin-right: 10px;
        }
    """) as interface:
        chat_history = gr.State([])

        # Title with logo on the left (updated to use the new image)
        with gr.Row():
            gr.Markdown("""
                <div class="header-title">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjaeoWoYgNtFCUn2u42Ih2J-UB2K8hCjlmCg&s" alt="Library Logo" />
                    서강대학교 로욜라 도서관 챗봇
                </div>
            """)

        # Chat history
        chatbot = gr.Chatbot(label="채팅 기록", elem_id="chat-container")

        # Input and buttons
        with gr.Row():
            user_input = gr.Textbox(
                placeholder="질문을 입력하세요",
                label="",
                lines=1,
                scale=8
            )
            send_btn = gr.Button("Send", elem_classes="send-button", scale=1)
            clear_btn = gr.Button("Clear", elem_classes="clear-button", scale=1)

        # Button events
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