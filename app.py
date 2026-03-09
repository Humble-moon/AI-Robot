import time
import datetime
import streamlit as st
from agent.react_agent import ReactAgent

# 设置页面配置
st.set_page_config(
    page_title="智扫通机器人智能客服",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主题配置
THEMES = {
    "橙色白色": {
        "primaryColor": "#FF6B00",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F5F5F5",
        "textColor": "#333333",
        "font": "sans serif"
    },
    "蓝色白色": {
        "primaryColor": "#1E88E5",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F5F5F5",
        "textColor": "#333333",
        "font": "sans serif"
    },
    "绿色白色": {
        "primaryColor": "#4CAF50",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F5F5F5",
        "textColor": "#333333",
        "font": "sans serif"
    },
    "深色模式": {
        "primaryColor": "#FF6B00",
        "backgroundColor": "#121212",
        "secondaryBackgroundColor": "#1E1E1E",
        "textColor": "#FFFFFF",
        "font": "sans serif"
    }
}

# 初始化主题
if "theme" not in st.session_state:
    st.session_state["theme"] = "橙色白色"

# 侧边栏
with st.sidebar:
    st.title("智扫通设置")
    
    # 主题选择
    theme = st.selectbox(
        "选择主题",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state["theme"])
    )
    
    if theme != st.session_state["theme"]:
        st.session_state["theme"] = theme
        st.rerun()
    
    # 应用主题
    theme_config = THEMES[st.session_state["theme"]]
    
    # 构建CSS字符串
    css = """
        <style>
        :root {
            --primary-color: %s;
            --background-color: %s;
            --secondary-background-color: %s;
            --text-color: %s;
            --border-color: rgba(0, 0, 0, 0.1);
            --shadow-color: rgba(0, 0, 0, 0.05);
        }
        
        body {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            writing-mode: horizontal-tb;
            direction: ltr;
            text-orientation: mixed;
        }
        
        /* 确保所有容器都使用横向排列 */
        * {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
            text-orientation: mixed !important;
        }
        
        /* 针对加载动画的容器 */
        .stSpinner {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对聊天输入框 */
        .stChatInput {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对侧边栏 */
        .stSidebar {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对聊天消息容器 */
        .stChatContainer {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对消息内容 */
        .stChatMessage > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对消息文本 */
        .stChatMessage > div > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对消息文本段落 */
        .stChatMessage > div > div > p {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
            white-space: normal !important;
        }
        
        /* 针对加载动画文本 */
        .stSpinner > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对加载动画容器 */
        .stSpinner {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
            display: inline-block !important;
        }
        
        /* 针对加载动画的父容器 */
        .st-emotion-cache-16idsys {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对所有可能的加载动画相关元素 */
        .st-emotion-cache-16idsys > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对消息容器 */
        .st-emotion-cache-1c7y2kd {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对消息内容 */
        .st-emotion-cache-1c7y2kd > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对消息文本 */
        .st-emotion-cache-1c7y2kd > div > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对Streamlit的所有容器 */
        .st-emotion-cache-13ln4jf {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对Streamlit的消息容器 */
        .st-emotion-cache-1c7y2kd {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对Streamlit的输入容器 */
        .st-emotion-cache-1c7y2kd {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对Streamlit的加载动画 */
        .st-emotion-cache-1vbkxwb {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对Streamlit的加载动画文本 */
        .st-emotion-cache-1vbkxwb > div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 针对Streamlit的所有div元素 */
        div {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
        }
        
        /* 确保文本不换行 */
        span {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
            white-space: nowrap !important;
        }
        
        /* 针对所有文本元素 */
        p, span, div, h1, h2, h3, h4, h5, h6 {
            writing-mode: horizontal-tb !important;
            direction: ltr !important;
            white-space: normal !important;
        }
        
        /* 主容器 */
        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* 消息样式 */
        .stChatMessage {
            border-radius: 18px;
            margin-bottom: 16px;
            padding: 16px 20px;
            animation: fadeIn 0.3s ease-in-out;
            box-shadow: 0 2px 8px var(--shadow-color);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
            writing-mode: horizontal-tb;
            direction: ltr;
        }
        
        .stChatMessage:hover {
            box-shadow: 0 4px 12px var(--shadow-color);
            transform: translateY(-1px);
        }
        
        .stChatMessage:nth-child(odd) {
            background-color: var(--secondary-background-color);
            color: var(--text-color);
            border-top-left-radius: 4px;
            border: 1px solid var(--border-color);
            font-weight: 500;
        }
        
        /* 确保用户消息在深色模式下也能清晰显示 */
        .stChatMessage:nth-child(odd) {
            color: var(--text-color) !important;
            background-color: var(--secondary-background-color) !important;
        }
        
        /* 针对Streamlit的实际聊天消息类 */
        .stChatMessage {
            color: var(--text-color) !important;
        }
        
        /* 确保输入框文字可见 */
        .stChatInput > div > div > input {
            color: var(--text-color) !important;
            background-color: var(--secondary-background-color) !important;
        }
        
        /* 针对Streamlit聊天消息的具体内容 */
        .stChatMessage > div > div > p {
            color: var(--text-color) !important;
        }
        
        /* 确保助手消息的文字颜色 */
        .stChatMessage:nth-child(even) > div > div > p {
            color: white !important;
        }
        
        /* 确保所有文本元素的颜色 */
        * {
            color: var(--text-color) !important;
        }
        
        /* 确保标题颜色 */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color) !important;
        }
        
        /* 确保侧边栏文本颜色 */
        .stSidebar * {
            color: var(--text-color) !important;
        }
        
        .stChatMessage:nth-child(even) {
            background-color: var(--primary-color);
            color: white;
            border-top-right-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* 动画效果 */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* 按钮样式 */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 12px;
            padding: 8px 16px;
            border: none;
            transition: all 0.3s ease;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .stButton > button:hover {
            background-color: %sCC;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* 选择框样式 */
        .stSelectbox > div > div {
            border-radius: 12px;
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            transition: all 0.2s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(255, 107, 0, 0.1);
        }
        
        /* 输入框样式 */
        .stChatInput > div > div > input {
            border-radius: 24px;
            border: 1px solid var(--border-color);
            padding: 12px 16px;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        
        .stChatInput > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(255, 107, 0, 0.1);
            outline: none;
        }
        
        /* 加载动画 */
        .stSpinner > div {
            border-top-color: var(--primary-color);
            width: 32px;
            height: 32px;
        }
        
        /* 侧边栏样式 */
        .stSidebar {
            background-color: var(--secondary-background-color);
            border-right: 1px solid var(--border-color);
        }
        
        /* 卡片样式 */
        .stInfo {
            border-radius: 12px;
            border: 1px solid var(--border-color);
            padding: 16px;
            background-color: var(--secondary-background-color);
            box-shadow: 0 2px 4px var(--shadow-color);
        }
        
        /* 标题样式 */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            line-height: 1.2;
            margin-bottom: 16px;
        }
        
        /* 分割线 */
        hr {
            border: none;
            height: 1px;
            background-color: var(--border-color);
            margin: 24px 0;
        }
        
        /* 聊天容器 */
        .stChatContainer {
            max-height: 600px;
            overflow-y: auto;
            padding: 10px;
        }
        
        /* 滚动条样式 */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--secondary-background-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-color);
        }
        </style>
        """ % (theme_config["primaryColor"], theme_config["backgroundColor"], 
                  theme_config["secondaryBackgroundColor"], theme_config["textColor"],
                  theme_config["primaryColor"])
    
    st.markdown(css, unsafe_allow_html=True)
    
    # 清除对话历史
    if st.button("清除对话历史"):
        st.session_state["message"] = []
        # 重新添加欢迎消息
        st.session_state["message"].append({"role": "assistant", "content": "你好！我是智扫通机器人智能客服，有什么可以帮助你的吗？", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        st.rerun()
    
    # 常见问题
    st.subheader("常见问题")
    common_questions = [
        "如何清洁扫地机器人",
        "扫地机器人迷路了怎么办",
        "扫地机器人电池续航多久",
        "如何选择适合的扫地机器人",
        "扫地机器人的噪音大吗"
    ]
    
    for q in common_questions:
        if st.button(q):
            # 添加用户消息
            user_message = {
                "role": "user", 
                "content": q, 
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state["message"].append(user_message)
            
            # 生成助手回答
            response_messages = []
            try:
                with st.spinner("智能客服思考中..."):
                    res_stream = st.session_state["agent"].execute_stream(q)

                    def capture(generator, cache_list):
                        try:
                            for chunk in generator:
                                cache_list.append(chunk)

                                for char in chunk:
                                    time.sleep(0.005)  # 减少延迟，提高响应速度
                                    yield char
                        except Exception as e:
                            yield f"处理过程中出现错误: {str(e)}"

                    # 显示助手消息
                    with st.chat_message("assistant", avatar="🤖"):
                        response = st.write_stream(capture(res_stream, response_messages))
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.caption(timestamp)
                    
                    # 保存助手消息
                    if response_messages:
                        assistant_message = {
                            "role": "assistant", 
                            "content": response_messages[-1], 
                            "timestamp": timestamp
                        }
                        st.session_state["message"].append(assistant_message)
                    else:
                        assistant_message = {
                            "role": "assistant", 
                            "content": "抱歉，处理您的请求时出现了错误，请稍后再试。", 
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state["message"].append(assistant_message)
            except Exception as e:
                st.error(f"系统错误: {str(e)}")
                assistant_message = {
                    "role": "assistant", 
                    "content": "抱歉，系统暂时无法处理您的请求，请稍后再试。", 
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state["message"].append(assistant_message)
            finally:
                st.rerun()
    
    # 关于系统
    st.subheader("关于系统")
    st.info("智扫通机器人智能客服系统 v1.1.0\n基于大语言模型和RAG技术\n为您提供专业的扫地机器人咨询服务")

# 主界面
st.markdown(f"""
<div style="text-align: center; margin-bottom: 40px;">
    <h1 style="font-size: 3rem; font-weight: 600; margin-bottom: 10px;">智扫通机器人智能客服</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 20px;">智能问答  ·  故障排查  ·  个性化服务</p>
    <div style="width: 100px; height: 3px; background-color: {theme_config['primaryColor']}; margin: 0 auto; margin-bottom: 20px;"></div>
    <p style="font-size: 1.5rem; font-weight: 300;">为您的扫地机器人提供专业支持</p>
</div>
""", unsafe_allow_html=True)

# 初始化会话状态
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []
    # 添加欢迎消息
    st.session_state["message"].append({"role": "assistant", "content": "你好！我是智扫通机器人智能客服，有什么可以帮助你的吗？", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

if "theme" not in st.session_state:
    st.session_state["theme"] = "橙色白色"

# 显示对话历史
for message in st.session_state["message"]:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])
        if "timestamp" in message:
            st.caption(message["timestamp"])

# 用户输入提示词
prompt = st.chat_input(placeholder="请输入你的问题，例如：如何清洁扫地机器人？")

if prompt:
    # 添加用户消息
    user_message = {
        "role": "user", 
        "content": prompt, 
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state["message"].append(user_message)
    
    # 显示用户消息
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
        st.caption(user_message["timestamp"])

    response_messages = []
    try:
        with st.spinner("智能客服思考中..."):
            res_stream = st.session_state["agent"].execute_stream(prompt)

            def capture(generator, cache_list):
                try:
                    for chunk in generator:
                        cache_list.append(chunk)

                        for char in chunk:
                            time.sleep(0.005)  # 减少延迟，提高响应速度
                            yield char
                except Exception as e:
                    yield f"处理过程中出现错误: {str(e)}"

            # 显示助手消息
            with st.chat_message("assistant", avatar="🤖"):
                response = st.write_stream(capture(res_stream, response_messages))
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.caption(timestamp)
            
            # 保存助手消息
            if response_messages:
                assistant_message = {
                    "role": "assistant", 
                    "content": response_messages[-1], 
                    "timestamp": timestamp
                }
                st.session_state["message"].append(assistant_message)
            else:
                assistant_message = {
                    "role": "assistant", 
                    "content": "抱歉，处理您的请求时出现了错误，请稍后再试。", 
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state["message"].append(assistant_message)
    except Exception as e:
        st.error(f"系统错误: {str(e)}")
        assistant_message = {
            "role": "assistant", 
            "content": "抱歉，系统暂时无法处理您的请求，请稍后再试。", 
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state["message"].append(assistant_message)
    finally:
        st.rerun()
