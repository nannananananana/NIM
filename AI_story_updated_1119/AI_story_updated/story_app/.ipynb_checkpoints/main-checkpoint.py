import ipywidgets as widgets
from IPython.display import display, clear_output, Image
from story_app import story_module1, story_module2  # 导入两个模型模块

class StoryApp:
    def __init__(self):
        # 模型介绍文本，使用 HTML 小部件
        self.intro_text = widgets.HTML(
            value="""
                <div style="font-size:18px; font-weight:bold; color:#0526D0; padding:10px 0; text-align:center;">
                    欢迎来到AI互动故事小助手！<br>
                    使用我们的两款语言模型，你可以选择不同类型的故事场景，在这里你可以自定义故事情节，生成专属于你的故事！<br>
                    开始你的新奇之旅吧！
                </div>
            """
        )

        # 模型选择按钮
        self.model1_button = widgets.Button(
            description="模型1️：llama3-8b",
            button_style='primary',
            layout=widgets.Layout(width='45%', height='40px', margin='5px')
        )
        self.model2_button = widgets.Button(
            description="模型2：mistral-7b",
            button_style='primary',
            layout=widgets.Layout(width='45%', height='40px', margin='5px')
        )

        # 选择模型后提示文本
        self.model_info = widgets.HTML(
            value="""
                <div style="font-size:18px; font-weight:bold; color:#0526D0; padding:10px 0; text-align:center;">
                    请从以上两个模型中选择一个开启神奇的AI之旅吧
                </div>
                <div style="font-size:12px; font-weight:bold; color:#000000; padding:10px 0; text-align:center;">
                    （不知道怎么选？没关系！每个模型都有各自的特点，但它们同样强大，跟着感觉走！）
                </div>
            """,
            layout=widgets.Layout(margin="10px 0")
        )

        # 标题标签
        self.story_type_label = widgets.Label(value="请先选择一个故事类型吧:", style={'font_weight': 'bold', 'font_size': '16px'})
        self.background_label = widgets.Label(value="自定义背景:", style={'font_weight': 'bold', 'font_size': '16px'})
        self.continue_label = widgets.Label(value="书写专属于你的故事:", style={'font_weight': 'bold', 'font_size': '16px'})
        
        # 初始化组件
        self.story_type_dropdown = widgets.Dropdown(
            options=[],  
            layout=widgets.Layout(width='100%')
        )
        self.background_input = widgets.Text(
            placeholder='发挥你的想象力创造属于你的人物背景！当然如果你想使用默认背景，留空即可（选择好后点击“开始”按钮以进入下一步）',
            layout=widgets.Layout(width='100%')
        )
        self.start_button = widgets.Button(
            description="马上出发！",
            button_style='success',
            layout=widgets.Layout(width='80%', height='35px', padding='5px 10px', margin='5px')
        )
        self.user_input = widgets.Text(
            placeholder='输入故事进展',
            layout=widgets.Layout(width='100%')
        )
        self.continue_button = widgets.Button(
            description="写好啦！",
            button_style='info',
            layout=widgets.Layout(width='48%', height='35px', margin='5px 2px 5px 0')
        )
        self.exit_button = widgets.Button(
            description="我不想玩了！现在就要退出！",
            button_style='danger',
            layout=widgets.Layout(width='48%', height='35px', margin='5px 0 5px 2px')
        )
        self.output_area = widgets.Output()

        # 初始化状态
        self.turn_count = 0
        self.model_prompt = ""
        self.current_module = None  # 当前选择的模型模块

        # 设置事件
        self.model1_button.on_click(self.select_model1)
        self.model2_button.on_click(self.select_model2)
        self.start_button.on_click(self.on_start_button_click)
        self.continue_button.on_click(self.on_continue_button_click)
        self.exit_button.on_click(self.on_exit_button_click)

    def select_model1(self, b):
        self.current_module = story_module1  # 选择 story_module1 作为当前模块
        self.model_info.value = """
                <div style="font-size:18px; font-weight:bold; color:#000000; padding:10px 0;">
                    已选择llama3-8b，即将开启新奇之旅！
                </div>
            """
        self.setup_story_module()

    def select_model2(self, b):
        self.current_module = story_module2  # 选择 story_module2 作为当前模块
        self.model_info.value =  """
                <div style="font-size:18px; font-weight:bold; color:#000000; padding:10px 0;">
                    已选择mistral-7b，即将开启新奇之旅！
                </div>
            """
        self.setup_story_module()

    def setup_story_module(self):
        # 加载故事类型选项
        self.story_type_dropdown.options = [(f"{key}: {value['user_intro'][:25]}...", key) for key, value in self.current_module.story_types.items()]

    def on_start_button_click(self, b):
        self.turn_count = 0  # 重置回合计数
        self.model1_button.disabled = True  # 禁用选择模型1按钮
        self.model2_button.disabled = True  # 禁用选择模型2按钮
        self.continue_button.disabled = False  # 启用“写好啦！”按钮
        self.exit_button.disabled = False  # 启用“我不想玩了！”按钮
        chosen_story = self.story_type_dropdown.value
        if self.background_input.value:
            self.model_prompt = self.background_input.value
        else:
            self.model_prompt = self.current_module.story_types[chosen_story]["model_prompt"]
        
        with self.output_area:
            clear_output()
            display(widgets.HTML(f"<b>故事类型:</b> {chosen_story}"))
            display(widgets.HTML(f"<b>背景:</b> {self.model_prompt}"))
            display(widgets.HTML("<hr>"))
            print("让我们开始故事吧！")

    def on_continue_button_click(self, b):
        user_text = self.user_input.value
        if user_text:
            response = self.current_module.get_story_response(self.model_prompt, user_text, self.turn_count)
            self.turn_count += 1
            with self.output_area:
                display(widgets.HTML(f"<b>你:</b> {user_text}"))
                display(widgets.HTML(f"<b style='color: blue;'>AI:</b> {response}"))
                display(widgets.HTML("<hr>"))
                
                self.user_input.value = ""  # 清空输入框
                
            if self.turn_count >= 6:
                self.continue_button.disabled = True
                print("故事已经接近尾声哦！")
                # 显示结束图片
                with self.output_area:
                    display(widgets.HTML("<b style='font-size:28px; color: red;'>结束啦，感谢您的体验！</b>"))
                    display(Image("story_app/image.jpg", width=300, height=200))

    def on_exit_button_click(self, b):
        self.model1_button.disabled = False  # 重新启用选择模型1按钮
        self.model2_button.disabled = False  # 重新启用选择模型2按钮
        with self.output_area:
            clear_output()
            display(widgets.HTML("<b style='font-size:28px; color: red;'>已退出哦，感谢您的体验！</b>"))
            display(Image("story_app/image.jpg", width=300, height=200))
        self.continue_button.disabled = True
        self.exit_button.disabled = True

    def display(self):
        # 布局设置：将模型选择、输入框和按钮放在一起
        controls = widgets.HBox([self.continue_button, self.exit_button])
        main_layout = widgets.VBox([
            self.intro_text,
            widgets.HBox([self.model1_button, self.model2_button]),
            self.model_info,  # 显示模型选择信息
            self.story_type_label,
            self.story_type_dropdown,
            self.background_label,
            self.background_input,
            self.start_button,
            self.output_area,
            self.continue_label,
            self.user_input,
            controls
        ])
        
        # 显示整体布局
        display(main_layout)
