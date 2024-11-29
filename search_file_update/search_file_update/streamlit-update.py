import streamlit as st
from openai import OpenAI
import os

def read_txt(file_path):
    """读取文本文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    # 页面标题和介绍
    st.title("LLM 学生体验 Demo - 从文章中寻找答案")
    
    # 第一部分：体验内容介绍
    st.header("一、体验内容介绍")
    
    st.write("""
    在本次体验中，我们将利用大语言模型（LLM）加载三篇文章，分别是朱自清的《背影》、鲁迅的《从百草园到三味书屋》
    以及《达芬奇简介 EN》。你可以针对文章内容进行提问，LLM 会根据文章内容生成答案。
    """)

    st.write("这个功能可能具备以下能力：")
    st.markdown("**智能阅读理解助手**：不仅能回答简单的问题，还能进行文章内容的分析、总结")
    st.markdown("**知识拓展与关联**：能够根据文章中的知识点，自动关联相关的背景知识")
    st.markdown("**个性化学习指导**：根据学生的提问和理解程度，提供个性化的学习建议")
    
    # 第二部分：语言模型介绍
    st.header("二、语言模型介绍")
    st.subheader("mistral-7b")
    st.write("""
    Mistral-7B-Instruct-v0.3 是一个能够遵循指令、完成请求并生成创造性文本格式的语言模型。
    它是 Mistral-7B-v0.3 生成文本模型的指令版本，使用各种公开可用的对话数据集进行了微调。
    """)

    # 初始化OpenAI客户端
    client = OpenAI(
        base_url=os.getenv("BASE_URL_MISTRAL"),
        api_key=os.getenv("API_KEY")
    )

    # 文档选择部分
    st.header("三、文档选择")
    doc_choice = st.selectbox(
        "请选择要阅读的文档：",
        ["从百草园到三味书屋", "达芬奇简介EN", "背影"]
    )
    
    if doc_choice:
        file_name = f"{doc_choice}.txt"
        try:
            document_content = read_txt(file_name)
            st.success(f"已加载文档：{doc_choice}")
            
            # 预设问题部分
            st.header("四、预设问题")
            preset_questions = [
                "这篇文章主要讲述了什么内容？",
                "作者在这篇文章中表达了怎样的情感？",
                "文章中的某个细节或描写给你留下了怎样的印象？"
            ]
            
            selected_question = st.selectbox(
                "选择预设问题：",
                preset_questions,
                key="preset_question"
            )
            
            if st.button("获取预设问题答案"):
                with st.spinner("AI正在思考..."):
                    prompt = (
                        "请根据文档内容回答此问题。\n\n"
                        f"问题: {selected_question}\n\n"
                        "以下是一个文档的内容片段：\n\n"
                        f"{document_content}"
                    )
                    
                    completion = client.chat.completions.create(
                        model="mistralai/mistral-7b-instruct-v0.3",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        top_p=0.7,
                        max_tokens=1024 * 2,
                        stream=True
                    )
                    
                    response_container = st.empty()
                    full_response = ""
                    for chunk in completion:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            response_container.markdown(full_response)
            
            # 自由提问部分
            st.header("五、自由提问")
            st.markdown("""
            在这里，你可以自由提问任何关于文章的问题。以下是一个写作示例：
            
            > **写作示例**：请按照选中的文章写一篇类似的文章。
            """)
            
            custom_question = st.text_area(
                "请输入你的问题：",
                height=100,
                placeholder="在这里输入你的问题..."
            )
            
            if st.button("提交自定义问题"):
                if custom_question:
                    with st.spinner("AI正在思考..."):
                        prompt = (
                            "请根据文档内容回答此问题。\n\n"
                            f"问题: {custom_question}\n\n"
			    "确保答案只包含与问题直接相关的信息，避免任何无关内容。\n\n"
			    "如果问题在文档中没有明确答案，则简洁地说 '未找到相关信息'。\n\n"
                            "如果问题中有字数要求，请严格按照要求生成内容。\n\n"
                            "以下是一个文档的内容片段：\n\n"
                            f"{document_content}"
                        )
                        
                        completion = client.chat.completions.create(
                            model="mistralai/mistral-7b-instruct-v0.3",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7,
                            top_p=0.7,
                            max_tokens=1024 * 2,
                            stream=True
                        )
                        
                        response_container = st.empty()
                        full_response = ""
                        for chunk in completion:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                response_container.markdown(full_response)
                else:
                    st.warning("请输入问题")
                    
        except FileNotFoundError:
            st.error("文档加载失败，请确认文件存在")

    st.markdown("""
    ## 六、体验总结

    在使用大语言模型（LLM）时，模型的回复往往具有一定的随机性。这种随机性源于模型的生成机制，即模型在生成文本时会基于概率分布选择下一个词或短语。这种随机性使得模型能够生成多样化的回复，但也可能导致回复的不一致性。

    ### 随机性的影响

    1. **多样性**：随机性使得模型能够生成多种可能的回复，增加了输出的多样性。
    2. **不确定性**：随机性可能导致模型在相同输入下生成不同的回复，增加了结果的不确定性。

    ### 控制随机性

    #### 增大随机性

    - **调整温度参数**：在生成文本时，可以通过调整温度参数（temperature）来增大随机性。温度参数越高，模型选择的词或短语的概率分布越平坦，生成的文本越多样化。
    - **增加样本数量**：通过生成多个样本并选择最合适的回复，可以增加随机性。

    #### 减小随机性

    - **降低温度参数**：降低温度参数可以使模型选择的词或短语的概率分布更集中，生成的文本更一致。
    - **使用确定性生成**：在某些情况下，可以使用确定性生成方法，确保模型在相同输入下生成相同的回复。

    ### 强调 `prompt` 的重要性

    `prompt` 在控制模型回复时起着至关重要的作用。通过精心设计的 `prompt`，可以引导模型生成符合特定要求的回复，减少随机性的影响。

    - **明确指令**：在 `prompt` 中明确指示模型需要完成的任务，可以显著提高回复的准确性。
    - **提供上下文**：通过提供足够的上下文信息，可以帮助模型更好地理解问题，生成更相关的回复。
    - **限制回复范围**：在 `prompt` 中设定回复的范围或格式，可以引导模型生成更符合预期的答案。

    ### 总结

    模型的随机性是其生成多样性回复的基础，但也可以通过调整参数和设计 `prompt` 来控制。通过合理利用 `prompt`，可以引导模型生成更符合要求的回复，减少随机性的负面影响。

    ### 感谢与愉快体验

    **感谢你的参与！** 希望你在本次 LLM 体验中感到愉快，并能对大语言模型（LLM）有一个更深入的了解。生成式 AI 的世界充满了无限可能，期待你在未来的学习和探索中继续发现更多精彩！
    """)
if __name__ == "__main__":
    main()
