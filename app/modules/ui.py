import gradio as gr

def build_ui(chatbot_interface):
    with gr.Blocks(css="""
    /* 서강체 폰트 로드 (Mac 및 Windows 대응) */
        @font-face {
            font-family: 'SogangMac';
            src: url('/app/modules/fonts/SOGANG_UNIVERSITY_for_mac.otf') format('opentype');
        }
        @font-face {
            font-family: 'SogangWindows';
            src: url('/app/modules/fonts/SOGANG_UNIVERSITY_for_windows.ttf') format('truetype');
        }
        body {
            font-family: 'SogangWindows', 'SogangMac', sans-serif;
            margin: 0;
            padding: 0;
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
            position: relative;
            z-index: 1;
        }
        .bot-message {
            background-color: #9C2A2A;  /* Lighter version of #861F1C */
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        .user-message, .user.svelte-u94xf4.message {
            background-color: rgba(134, 31, 28, 0.1);  /* 배경색 투명도 10% */
            border: 1px solid rgba(134, 31, 28, 0.2);  /* 테두리 색상, 두께, 투명도 설정 */
            border-radius: 10px;  /* 둥근 모서리 적용 */
            padding: 10px;
            color: white;  /* 글자 색상 */
            font-weight: bold;
        }
        .header-title {
            display: flex;
            align-items: center;
            font-family: 'SogangWindows', 'SogangMac', sans-serif;  /* Mac 및 Windows 폰트 적용 */
            font-size: 36px;  /* 글씨 크기 증가 */
            font-weight: bold; /* 굵게 */
        }
        .header-title img {
            width: 180px;  /* Adjust icon size */
            height: auto;
            margin-right: 10px;
        }
        /* 채팅방 배경 이미지 및 흐림 효과 */
        .chat-container {
            position: relative;
            background-image: url('https://i.namu.wiki/i/cQrk_1k9GWhb6dNzDu6zmT5qZajKV_t6dWbnas2NugXkNq8DZr6z3iJkZuUThjao7eUURuvCQmfvme4uUGMpRA.webp');
            background-size: cover;
            background-position: center;
            filter: blur(5px);  /* 흐림 효과 적용 */
        }

        /* 메시지 영역을 배경 이미지 위에 표시되도록 z-index 설정 */
        .chat-container .message-container {
            position: relative;
            z-index: 2;  /* 메시지가 배경 이미지 위에 오도록 설정 */
        }
    """) as interface:
        
        chat_history = gr.State([])  # chat_history 정의

        # Title with logo on the left (updated to use the new image)
        with gr.Row():
            gr.HTML("""
                <div class="header-title">
                    <img src="https://sogang.bookcosmos.com/logoImg/logo.gif" 
                        alt="Library Logo" 
                        style="cursor: pointer;" 
                        onclick="location.reload();" />
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
