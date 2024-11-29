import ipywidgets as widgets
from IPython.display import display, clear_output, Audio
import subprocess

class SpeechToTextApp:
    def __init__(self):
        # 可选择的音频文件列表
        self.audio_files = {
            "Ed Sheeran - Galway Girl": "audios/Ed Sheeran-galway girl.wav",
            "Ed Sheeran - Sing": "audios/Ed Sheeran-sing.wav",
            "Eminem - Lose Yourself": "audios/Eminem-lose yourself.wav",
            "Soccer Commentary 1": "audios/Soccer Commentary1.wav",
            "Soccer Commentary 2": "audios/Soccer Commentary2.wav"
        }

        # 创建音频选择下拉菜单
        self.audio_dropdown = widgets.Dropdown(
            options=list(self.audio_files.keys()),
            description="选择音频：",
            layout=widgets.Layout(width='40%')
        )

        # 转换按钮
        self.transcribe_button = widgets.Button(
            description="转换文字",
            button_style='primary',
            layout=widgets.Layout(width='30%', height='40px', margin='10px 0')
        )

        # 播放器区域
        self.player_area = widgets.Output()

        # 转录结果输出区域
        self.output_area = widgets.Output()

        # 绑定事件
        self.audio_dropdown.observe(self.update_player, names='value')
        self.transcribe_button.on_click(self.transcribe_audio)

        # 默认加载选中的音频文件
        self.current_audio_path = self.audio_files[self.audio_dropdown.value]
        self.update_player()

    def update_player(self, change=None):
        # 更新播放器并显示当前音频
        self.current_audio_path = self.audio_files[self.audio_dropdown.value]
        with self.player_area:
            clear_output()
            display(Audio(self.current_audio_path, autoplay=False))
    
    def transcribe_audio(self, b):
        # 清除输出区域并显示转换状态
        with self.output_area:
            clear_output()
            display(widgets.HTML("<p style='font-size:16px; color:blue;'>正在转换文字，请稍候...</p>"))

        # ASR 模型命令
        command = [
            "python3", "python-clients/scripts/asr/transcribe_file.py",
            "--server", "10.244.0.149:50051",
            "--language-code", "en-US",
            "--input-file", self.current_audio_path
        ]

        # 执行命令
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            transcription = result.stdout
            with self.output_area:
                clear_output()
                display(widgets.HTML(f"<p style='font-size:16px; color:green;'>转换结果:</p>"))
                display(widgets.HTML(f"<p style='font-size:14px;'>{transcription}</p>"))
        except subprocess.CalledProcessError as e:
            with self.output_area:
                clear_output()
                display(widgets.HTML(f"<p style='font-size:16px; color:red;'>转换失败: {e}</p>"))

    def display(self):
        # 布局
        display(widgets.VBox([
            widgets.HTML(value="""
                <div style="font-size:18px; font-weight:bold; color:#000000; padding:10px 0">
                    Hello！这是你的“AI音频转文字小助手” 
                </div>
                <div style="font-size:18px; font-weight:bold; color:#000000; padding:10px 0">
                    快来试试看吧！
                </div>
            """),
            self.audio_dropdown,
            self.player_area,  # 显示播放器区域
            self.transcribe_button,
            self.output_area
        ]))
