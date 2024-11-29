import streamlit as st
from datetime import datetime
from story_app import story_module1, story_module2

# 初始化
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
if "context" not in st.session_state:  
    st.session_state["context"] = []
if "is_generating" not in st.session_state:  # 是否正在生成内容的状态
    st.session_state["is_generating"] = False
if "generate_message" not in st.session_state:
    st.session_state["generate_message"] = ""  # 新增变量，用于动态提示

st.markdown("""
# 大语言模型（LLM）学生体验 Demo - AI story

## 1. 体验内容介绍

在这个体验中，我们将通过大语言模型（LLM）生成不同主题的故事。我们预设了10个场景，分别是：

- 冒险
- 奇幻
- 科幻
- 悬疑
- 恐怖
- 历史
- 爱情
- 神秘
- 职场
- 禁忌

希望通过不同主题的故事风格，你能对 LLM 的生成能力有一个初步的体验。

## 2. 大语言模型介绍

本次体验将包括两个大语言模型，分别是 `llama-3.1-8b` 和 `mistral-7b`。以下是这两个模型的中文描述：

### Llama-3.1-8b

Llama 3 是一个大型语言 AI 模型，包含一系列能够根据提示生成文本和代码的模型。Meta 开发并发布了 Meta Llama 3 系列大型语言模型（LLMs），这是一系列预训练和指令微调的生成文本模型，有 8B 和 70B 两种规模。标记数量仅指预训练数据。8B 和 70B 版本都使用 Grouped-Query Attention (GQA) 来提高推理的可扩展性。Llama 3 指令微调模型针对对话用例进行了优化，在许多常见的行业基准测试中优于许多可用的开源聊天模型。此外，在开发这些模型时，我们非常注重优化有用性和安全性。

### Mistral-7b

Mistral-7B-Instruct-v0.3 是一个能够遵循指令、完成请求和生成创意文本格式的语言模型。它是 Mistral-7B-v0.3 生成文本模型的指令版本，使用多种公开可用的对话数据集进行了微调。

我们希望通过选择不同的模型，来体会不同模型的能力差异。

## 3. 开始体验

接下来是真正的体验环节！开启你的奇妙之旅吧。
""")

# 选择模型
st.markdown("### 第1️⃣步：选择模型")
selected_model = st.selectbox("在llama-3.1-8b和mistral-7bz中选一个吧！（不知道选什么没关系，每个模型都有自己的特点！）", ["模型1️：llama-3.1-8b", "模型2：mistral-7b"])
if selected_model == "模型1️：llama-3.1-8b":
    st.session_state["current_module"] = story_module1
else:
    st.session_state["current_module"] = story_module2

# 选择故事类型
st.markdown("### 第2️⃣步：选择故事类型")
story_type_options = [(f"{key}: {value['user_intro'][:25]}...", key) for key, value in st.session_state["current_module"].story_types.items()]
story_type_dict = dict(story_type_options)
selected_story_type = st.selectbox("请从以下列表中选择一个感兴趣的故事类型", list(story_type_dict.keys()))
st.session_state["chosen_story_key"] = story_type_dict[selected_story_type]

# 输入背景设定
st.markdown("### 第3️⃣步：自定义你的故事背景")
background_input = st.text_input("发挥你的想象力创造属于你的人物背景！或留空使用默认背景")

# 开始故事按钮
if st.button("马上出发！"):
    st.session_state["turn_count"] = 0
    st.session_state["story_content"] = ""  # 重置故事内容
    st.session_state["context"] = []  # 重置上下文
    st.session_state["model_prompt"] = (
        background_input if background_input 
        else st.session_state["current_module"].story_types[st.session_state["chosen_story_key"]]["model_prompt"]
    )
    st.session_state["context"].append(st.session_state["model_prompt"])  # 初始化上下文

    # 显示故事类型和背景
    st.session_state["show_story_info"] = True

# 持续显示故事类型和背景
if "show_story_info" in st.session_state and st.session_state["show_story_info"]:
    st.markdown(f"#### 故事类型: {selected_story_type}")
    st.markdown(f"#### 背景: {st.session_state['model_prompt']}")

# 继续故事
st.markdown("### 第4️⃣步：书写专属于你的故事")
user_input = st.text_input("输入故事进展:每次生成完新的内容后，可以再继续输入内容以续写哦！", "")

# 写好啦按钮，生成故事内容并添加到滚动框
if st.button("写好啦！(点击后右上角会显示“RUNNING”请耐心等待哦)") and user_input:
    st.session_state["is_generating"] = True  # 开始生成内容

    # 添加用户输入到上下文
    st.session_state["context"].append(f"你: {user_input}")
    st.session_state["story_content"] += f"**你**: {user_input}\n\n"

    # 调用生成故事内容的函数
    response = st.session_state["current_module"].get_story_response(st.session_state["context"], st.session_state["turn_count"])
    
    # 更新上下文和回合数
    st.session_state["context"].append(f"AI: {response}")
    st.session_state["turn_count"] += 1
    st.session_state["is_generating"] = False  
    st.session_state["generate_message"] = "<p style='color: green;'>如果要继续生成故事内容，请在👆框内重新输入文字哦！</p>"  

    # 累积显示生成的故事内容
    st.session_state["story_content"] += f"**AI**: {response}\n\n"

    # 显示故事即将结束的提示
    if st.session_state["turn_count"] >= 3:
        st.write("故事已经接近尾声哦！")

# 在生成和完成状态之间动态显示不同的消息
st.markdown(st.session_state["generate_message"], unsafe_allow_html=True)

# 将故事内容显示在一个滚动框中
st.markdown("### 故事内容")
st.markdown(
    "<div style='overflow-y: auto; height: 400px; padding: 10px; border: 1px solid #ddd;'>" +
    st.session_state['story_content'].replace('\n', '<br>') +
    "</div>",
    unsafe_allow_html=True
)

if st.session_state["story_content"]:
    # 准备格式化的下载内容
    formatted_story = f"""
====================================================
                AI 故事生成器 - 我的故事
====================================================

创作时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
使用模型: {selected_model}

----------------------------------------------------
故事信息
----------------------------------------------------
故事类型: {selected_story_type}
背景设定: {st.session_state['model_prompt']}

----------------------------------------------------
故事内容
----------------------------------------------------

{st.session_state['story_content']}

====================================================
        感谢使用 AI 故事生成器！
====================================================
"""
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        # 添加下载按钮
        st.download_button(
            label="📥 保存我的故事",
            data=formatted_story,
            file_name=f"AI_Story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            help="点击下载生成的故事内容",
            key="download_button"
        )
    
    with col2:
        # 退出按钮
        if st.button("我不想玩了！现在就要退出！"):
            st.session_state["story_content"] = ""
            st.session_state["model_prompt"] = ""
            st.session_state["show_story_info"] = False
            st.session_state["context"] = []  # 清空上下文
            st.markdown("<b style='font-size:24px; color: red;'>已退出哦，感谢您的体验！</b>", unsafe_allow_html=True)
            st.image("story_app/image.jpg", width=300)

st.markdown("""
## 4. 体验总结

### 大语言模型（LLM）的局限性

在体验过程中，你可能会发现不同模型生成的故事有所差异，这很正常。大语言模型（LLM）本身存在一些局限性，例如：

- **数据集规模限制**：模型的表现受限于训练数据的规模和质量。
- **模型参数量限制**：模型的参数量决定了其表达能力和复杂性，但也会影响推理速度和资源消耗。
- **幻觉问题**：模型可能会生成看似合理但实际上不准确或不存在的信息。
- **其他限制**：模型在处理特定任务时可能会有其他局限性，如对特定领域的理解不足等。

### 生成式 AI 的其他强大能力

除了生成故事，生成式 AI 还有许多其他强大的能力，例如：

- **文本生成**：生成文章、诗歌、对话等。
- **代码生成**：自动生成代码片段或完整的程序。
- **图像生成**：根据文本描述生成图像。
- **语音合成**：将文本转换为自然语音。
- **数据增强**：生成用于训练和测试的数据集。

**感谢你的参与！** 希望你在本次 LLM 体验中感到愉快，并能对大语言模型（LLM）有一个更深入的了解。生成式 AI 的世界充满了无限可能，期待你在未来的学习和探索中继续发现更多精彩！
"""    
)
