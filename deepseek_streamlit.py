import requests
import streamlit as st

st.title('Deepseek Chatbot')

# 侧边栏输入 API 密钥
with st.sidebar:
    api_key = st.text_input("请输入你的 DeepSeek API 密钥", type="password")
    base_url = 'https://api.deepseek.com/v1'

    st.write("选择模型:")

    # 模型选择
    model = st.selectbox("模型", ["deepseek-coder", "deepseek-chat"])

    st.write("调整参数:")

    # 根据选择的模型设置默认 temperature
    default_temperature = 1.0 if model == "deepseek-coder" else 1.0

    # 温度参数
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=default_temperature, step=0.1, help="""
    对于不同使用场景，我们建议设置如下温度值：
    - 代码生成/数学解题：0.0
    - 数据抽取/分析：0.7
    - 通用对话：1.0
    - 翻译：1.1
    - 创意类写作/诗歌创作：1.25
    """)

    # 最大输出长度
    max_tokens = st.slider("Max Tokens", min_value=1, max_value=4096, value=1500, step=50)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Enter your message:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": st.session_state.messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }

    response = requests.post(f"{base_url}/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        msg = response_data['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
