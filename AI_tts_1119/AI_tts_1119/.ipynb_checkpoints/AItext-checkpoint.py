import ipywidgets as widgets
from IPython.display import display, clear_output, Audio
import subprocess

class TTSApp:
    def __init__(self):
        # 文本输入框
        self.text_input = widgets.Textarea(
            placeholder="输入您希望转为语音的文本",
            layout=widgets.Layout(width='80%', height='100px')
        )

        # 声音类型选择下拉菜单
        self.voice_dropdown = widgets.Dropdown(
            options=[
                "English-US.Female-1", "English-US.Male-1", "English-US.Female-Neutral",
                "English-US.Male-Neutral", "English-US.Female-Angry", "English-US.Male-Angry",
                "English-US.Female-Calm", "English-US.Male-Calm", "English-US.Female-Fearful",
                "English-US.Female-Happy", "English-US.Male-Happy", "English-US.Female-Sad"
            ],
            description="声音类型",
            layout=widgets.Layout(width='80%')
        )

        # 生成语音按钮
        self.generate_button = widgets.Button(
            description="生成语音",
            button_style='success',
            layout=widgets.Layout(width='30%', height='40px', margin='10px 0')
        )
        
        # 输出区域
        self.output_area = widgets.Output()

        # 设置事件处理程序
        self.generate_button.on_click(self.on_generate_button_click)
        
        # 音频路径
        self.audio_path = "audio.wav"

    def on_generate_button_click(self, b):
        # 清除之前的输出
        with self.output_area:
            clear_output()
            print("正在生成语音，请稍候...")

        # 获取用户输入的文本和选择的声音类型
        text = self.text_input.value
        voice = self.voice_dropdown.value

        # 如果文本为空，则提示用户输入文本
        if not text:
            with self.output_area:
                clear_output()
                print("请输入需要转换的文本内容")
            return
        
        # 生成语音命令
        command = [
            "python", "python-clients/scripts/tts/talk.py",
            "--server", "grpc.nvcf.nvidia.com:443", "--use-ssl",
            "--metadata", "function-id", "0149dedb-2be8-4195-b9a0-e57e0e14f972",
            "--metadata", "authorization", "Bearer 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",
            "--text", text,
            "--voice", voice,
            "--output", self.audio_path
        ]
        
        # 执行命令生成语音
        try:
            subprocess.run(command, check=True)
            with self.output_area:
                clear_output()
                print("语音文件生成成功！您可以使用下方播放器进行播放。")
                display(Audio(self.audio_path))
        except subprocess.CalledProcessError as e:
            with self.output_area:
                clear_output()
                print(f"语音文件生成失败：{e}")

    def display(self):
        # 显示组件
        display(widgets.VBox([
            widgets.HTML(value="""
                <div style="font-size:18px; font-weight:bold; color:#000000; padding:10px 0">
                    Hello！这是你的“AI文字转语音小助手”，在这里您还能体验到不同情绪的语音表达
                    快来试试看吧！
                </div>
            """),
            self.text_input,
            self.voice_dropdown,
            self.generate_button,
            self.output_area
        ]))