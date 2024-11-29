import re
import streamlit as st
import subprocess
from pydub import AudioSegment
from io import BytesIO
import os

# 音频文件列表
audio_files = {
    "Ed Sheeran - Galway Girl": "audios/Ed Sheeran-galway girl.wav",
    "Ed Sheeran - Sing": "audios/Ed Sheeran-sing.wav",
    "Eminem - Lose Yourself": "audios/Eminem-lose yourself.wav",
    "Soccer Commentary 1": "audios/Soccer Commentary1.wav",
    "Soccer Commentary 2": "audios/Soccer Commentary2.wav"
}


# 显示 Markdown 内容
st.markdown("""
# 大语言模型（LLM）学生体验 Demo - Speech to Text

## 1. 体验内容介绍
今天，我们将带你体验一款由 NVIDIA NIM 驱动的语音转文字（ASR） DEMO。这款 DEMO 通过录制或选择预设的音频文件，将语音实时转化为文字，让你直观地体验到大语言模型在语音识别和文本生成方面的强大能力。

不同于传统的语音识别系统，这款模型能够精准捕捉语音中的细微差异，并将其转化为流畅的文字。无论是说唱音乐、体育解说还是复杂的技术术语，模型都能高效地将语音内容转化为准确的文字。

## 2. 大语言模型介绍
本次体验的语音转文字模型是基于 Parakeet 和 NeMo 的 ASR 模型：

Parakeet 是对会话式 AI 发展的一次重大突破，拥有卓越的识别准确率。结合 NeMo 框架的灵活性和易用性，开发者可以轻松创建更自然、直观的语音驱动应用。这不仅能提升虚拟助手的准确性，还能支持流畅的实时交流。无论是改进语音助手的识别率还是实现无缝的实时沟通，Parakeet 模型为语音识别应用开辟了更多的可能性。

## 3. 开始体验
接下来是正式的体验环节！在下拉菜单中你可以选择不同的音频类型进行体验，开始你的AI之旅吧！
""")

# 创建页面标题
#st.title("语音转文字 Demo")

# 选择音频文件下拉菜单
st.markdown("<h3 style='color: blue; font-size: 24px;'>请先选择一段音频吧</h3>", unsafe_allow_html=True)
selected_audio = st.selectbox("", list(audio_files.keys()))
audio_path = audio_files[selected_audio]

# 播放选中的音频文件
st.audio(audio_path, format="audio/wav")

# 转换按钮
if st.button("转换文字"):
    st.write("正在转换文字，请稍候...")
    
    endpoint_pre = os.getenv("ENTRY_URL")
    endpoint = re.sub(r'^https?://', '', endpoint_pre)

    # ASR 模型调用命令
    command = [
        "python3", "python-clients/scripts/asr/transcribe_file.py",
        "--server", endpoint,
        "--language-code", "en-US",
        "--input-file", audio_path,
        "--use-ssl",
    ]

    # 执行命令并捕获输出
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        transcription = result.stdout
        st.success("转换成功！以下是转录的内容：")
        st.text_area("转录结果", transcription, height=200)
    except subprocess.CalledProcessError as e:
        st.error(f"转换失败：{e}")


st.markdown("""
## 4. 语音转文字（ASR）体验总结

### 通过本次体验，我们可以了解到：

- **语音识别的精准度与适应性**
：您会发现，ASR 系统能够准确识别各种音频内容，不论是带有口音的对话、快速的播报，还是嘈杂环境中的语音。ASR 模型的准确率直接影响到识别结果的质量，而高性能的 ASR 系统能够捕捉到细微的语音特征，将其转化为准确的文字输出。

- **语音识别的多样应用**
：ASR 系统在不同领域展现出广泛的应用潜力，例如智能语音助手、实时字幕、会议纪要生成等。本次体验展示了 ASR 模型在应对不同类型音频内容上的强大适应性，让您能够切身体验到它的实际应用效果。

- **实时性和处理速度**
：您会体验到 ASR 系统的实时性和响应速度。优质的 ASR 系统能够在短时间内快速完成语音转录，保证用户体验的流畅性。处理速度的提升使得语音识别技术在更多实时应用中具有可行性，如实时翻译和字幕生成。

- **ASR 系统的多层次处理架构**
：ASR 系统的处理流程通常包括音频预处理、特征提取、语言模型和解码等多个阶段。NeMo 框架赋予了模型高度的灵活性，使开发者能够轻松进行自定义和调优，以满足不同应用场景的需求。体验过程让我们更直观地理解了 ASR 系统是如何逐步将语音信号转化为准确的文字。

**感谢您的参与！** 
希望您在本次 ASR 体验中有所收获，对语音转文字技术有更深入的理解。生成式 AI 的领域充满着无限可能，期待您在未来的学习和探索中继续发现更多精彩应用！
""")