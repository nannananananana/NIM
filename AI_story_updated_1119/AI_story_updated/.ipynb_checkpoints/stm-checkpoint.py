import streamlit as st
from story_app import story_module1, story_module2  # 导入两个模型模块

# 初始化持久化变量以便保持故事内容和背景介绍
if "story_content" not in st.session_state:
    st.session_state["story_content"] = ""
if "model_prompt" not in st.session_state:
    st.session_state["model_prompt"] = ""
if "current_module" not in st.session_state:
    st.session_state["current_module"] = None
if "chosen_story_key" not in st.session_state:
    st.session_state["chosen_story_key"] = ""
if "turn_count" not in st.session_state:
    st.session_state["turn_count"] = 0

# 介绍文本
st.markdown("""
<div style="text-align:center; color:#0526D0; font-size:24px;">
    欢迎来到AI互动故事小助手！<br>
    使用我们的两款语言模型，你可以选择不同类型的故事场景，生成专属于你的故事！<br>
    开始你的新奇之旅吧！
</div>
""", unsafe_allow_html=True)

# 选择模型
st.markdown("### 第1️⃣步：选择模型")
selected_model = st.selectbox("选择模型", ["模型1️：llama3-8b", "模型2：mistral-7b"])
if selected_model == "模型1️：llama3-8b":
    st.session_state["current_module"] = story_module1
else:
    st.session_state["current_module"] = story_module2

# 选择故事类型
st.markdown("### 第2️⃣步：选择故事类型")
story_type_options = [(f"{key}: {value['user_intro'][:25]}...", key) for key, value in st.session_state["current_module"].story_types.items()]
story_type_dict = dict(story_type_options)
selected_story_type = st.selectbox("请选择一个感兴趣的故事类型", list(story_type_dict.keys()))
st.session_state["chosen_story_key"] = story_type_dict[selected_story_type]

# 输入背景设定
st.markdown("### 第3️⃣步：自定义你的故事背景")
background_input = st.text_input("发挥你的想象力创造属于你的人物背景！或留空使用默认背景")

# 开始故事按钮
if st.button("马上出发！"):
    st.session_state["turn_count"] = 0
    st.session_state["story_content"] = ""  # 重置故事内容
    st.session_state["model_prompt"] = (
        background_input if background_input 
        else st.session_state["current_module"].story_types[st.session_state["chosen_story_key"]]["model_prompt"]
    )

    # 显示故事类型和背景
    st.session_state["show_story_info"] = True  # 设定标志用于后续显示控制

# 持续显示故事类型和背景
if "show_story_info" in st.session_state and st.session_state["show_story_info"]:
    st.markdown(f"#### 故事类型: {selected_story_type}")
    st.markdown(f"#### 背景: {st.session_state['model_prompt']}")

# 继续故事
st.markdown("### 第4️⃣步：书写专属于你的故事")
user_input = st.text_input("输入故事进展", "")

# 写好啦按钮，生成故事内容并添加到滚动框
if st.button("写好啦！") and user_input:
    # 调用生成故事内容的函数，显示“生成中”的提示
    st.session_state["story_content"] += f"**你**: {user_input}\n\n"
    st.write("生成中，请稍候...")

    # 生成故事内容
    response = st.session_state["current_module"].get_story_response(
        st.session_state["model_prompt"], user_input, st.session_state["turn_count"]
    )
    
    # 更新回合数
    st.session_state["turn_count"] += 1

    # 累积显示生成的故事内容
    st.session_state["story_content"] += f"**AI**: {response}\n\n"

    # 显示故事即将结束的提示
    if st.session_state["turn_count"] >= 6:
        st.write("故事已经接近尾声哦！")

# 将故事内容显示在一个滚动框中
st.markdown("### 故事内容")
st.markdown(
    f"<div style='overflow-y: auto; height: 300px; padding: 10px; border: 1px solid #ddd;'>"
    f"{st.session_state['story_content'].replace('\n', '<br>')}"
    f"</div>", 
    unsafe_allow_html=True
)

# 退出故事
if st.button("我不想玩了！现在就要退出！"):
    st.session_state["story_content"] = ""
    st.session_state["model_prompt"] = ""
    st.session_state["show_story_info"] = False
    st.markdown("<b style='font-size:24px; color: red;'>已退出哦，感谢您的体验！</b>", unsafe_allow_html=True)
    st.image("story_app/image.jpg", width=300)
