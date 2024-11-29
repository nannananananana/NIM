import streamlit as st
import subprocess

# 介绍文本
st.markdown("""
# 大语言模型（LLM）学生体验 Demo - Text to Speech

## 1. 体验内容介绍

今天，我们将带你体验一款由 NVIDIA NIM 驱动的文字转语音 DEMO，这款 DEMO 不仅限于简单的语音合成，通过下拉菜单，你可以轻松选择不同的情感模式，如欢快、悲伤、严肃等，感受模型在生成语音时如何巧妙地调整语调，让每一句话都充满情感色彩。

无需复杂的设置，只需几步操作，你就能实时体验到模型生成的语音效果。

## 2. 大语言模型介绍

本次体验应用的模型是 `fastpitch-hifigan-tts`：

English-US Multispeaker FastPitch-HifiGAN是一个将文字转成语音的模型，它包括两个部分：FastPitch和HifiGAN。
FastPitch是个梅尔频谱图生成器，专门用来和神经声码器一起，作为文本到语音系统的第一个部分。它用国际音标（IPA）来做推理和训练，而且可以生成美国英语的男声或女声。
HifiGAN是个神经声码器模型，专门用在文本到语音的应用里。它是两阶段语音合成流程的第二部分。

## 3. 开始体验

接下来是真正的体验环节！现在就开始输入你的内容吧！

""", unsafe_allow_html=True)

# 文本输入框
text_input = st.text_area("输入您希望转为语音的文本", height=100, placeholder="输入您希望转为语音的文本")

# 声音类型选择下拉菜单
voice = st.selectbox(
    "选择声音类型",
    [
        "English-US.Female-1", "English-US.Male-1", "English-US.Female-Neutral",
        "English-US.Male-Neutral", "English-US.Female-Angry", "English-US.Male-Angry",
        "English-US.Female-Calm", "English-US.Male-Calm", "English-US.Female-Fearful",
        "English-US.Female-Happy", "English-US.Male-Happy", "English-US.Female-Sad"
    ]
)

# 输出的音频文件路径
audio_path = "audio.wav"

# 生成语音的按钮
if st.button("生成语音"):
    # 检查用户是否输入了文本
    if not text_input:
        st.error("请输入需要转换的文本内容")
    else:
        # 显示生成中状态
        st.info("正在生成语音，请稍候...")

        # 生成语音命令
        command = [
            "python", "python-clients/scripts/tts/talk.py",
            "--server", "grpc.nvcf.nvidia.com:443", "--use-ssl",
            "--metadata", "function-id", "0149dedb-2be8-4195-b9a0-e57e0e14f972",
            "--metadata", "authorization", "Bearer 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",
            "--text", text_input,
            "--voice", voice,
            "--output", audio_path
        ]
        
        # 执行命令生成语音
        try:
            subprocess.run(command, check=True)
            st.success("语音文件生成成功！您可以使用下方播放器进行播放。")
            st.markdown("<p style='font-size:14px;'>点击播放按钮来听听效果（最右侧按钮还能进行下载哦！）</p>", unsafe_allow_html=True)
            st.audio(audio_path)
        except subprocess.CalledProcessError as e:
            st.error(f"语音文件生成失败：{e}")

st.markdown("""
## 4. 体验完毕后的总结

### 通过本次体验我们可以了解到

- **语音合成的多样性**：
  - 您会发现TTS系统能够生成多种语音风格，如男声、女声，以及不同情感的语调（如欢快、悲伤、严肃等）。
  - 通过选择不同的语音风格，您可以体验到模型如何根据输入的文本生成不同风格的语音。

- **语音的自然度和流畅度**：
  - 您会注意到生成的语音在自然度和流畅度上的表现。高质量的TTS系统能够生成接近自然人声的语音，而低质量的系统可能会出现不自然的停顿、发音错误或语调不协调。

- **实时性和响应速度**：
  - 您会体验到TTS系统的实时性和响应速度。优秀的TTS系统能够在短时间内生成高质量的语音，而较慢的系统可能会导致延迟。

- **文本到语音的转换过程**：
  - 您会了解到TTS系统通常由两个主要部分组成：文本分析模块（如FastPitch）和语音合成模块（如HifiGAN）。文本分析模块将输入的文本转换为中间表示（如梅尔频谱图），而语音合成模块将中间表示转换为最终的语音输出。

**感谢你的参与！** 希望你在本次 TTS 体验中感到愉快，并能对文字转语音技术有一个更深入的了解。生成式 AI 的世界充满了无限可能，期待你在未来的学习和探索中继续发现更多精彩！

""", unsafe_allow_html=True)
