import tkinter as tk
from tkinter import ttk # Import ttk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk
import tkinter.font as tkFont
from travel_hamster_utils import CapsuleButton, BG_COLOR, PRIMARY_COLOR, icon_images, load_icons
from openai import OpenAI
import webbrowser

def show_third_window(root, startplace, destination, startyear, startmonth, startdate, days, hotel_list, hotel_link_list, restaurant_list, restaurant_link_list, train_link, air_link, nav_info, spot_list):
    window2 = tk.Toplevel(root)
    window2.title("travel hamster")
    window2.geometry("1000x650+250+100")
    window2.configure(bg=BG_COLOR)

    top_frame = tk.Frame(window2, bg=BG_COLOR)
    top_frame.pack(fill=tk.X)
    # 这个 Frame 将作为蓝色的标题背景条，并横向填充
    title_line_frame = tk.Frame(top_frame, bg=PRIMARY_COLOR)
    # 横向填充，同时为蓝色条本身添加垂直外边距和水平内边距
    title_line_frame.pack(fill=tk.X, pady=10, padx=10) 

    # Wrapper frame to center the content (icon + text) within title_line_frame
    content_wrapper_frame = tk.Frame(title_line_frame, bg=PRIMARY_COLOR) # 继承蓝色背景
    content_wrapper_frame.pack() # 这会使得 content_wrapper_frame 在 title_line_frame 中居中

    # 标题文字标签
    # 文字标签背景也是 PRIMARY_COLOR，文字颜色为白色
    text_label = tk.Label(content_wrapper_frame, text="Welcome to travel hamster~!", font=('Arial', 16), bg=PRIMARY_COLOR, fg="white", pady=5)
    text_label.pack(side='left') # 文字在 wrapper 内紧随图标
    #tk.Label(top_frame, text="").pack()
    tk.Label(top_frame, text="铛铛！以下是小仓鼠为你准备的旅行攻略~", font=('Arial', 12, 'bold'), bg=BG_COLOR, fg='black').pack()
    tk.Label(top_frame, text="💙请查收₍ᐢ..ᐢ₎♡", font=('Arial', 12, 'bold'), bg=BG_COLOR, fg='black').pack()

    frame = tk.Frame(window2, bg=BG_COLOR)
    frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    load_icons() # 加载图标资源
    canvas = tk.Canvas(frame, bg=BG_COLOR)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    inner_frame = tk.Frame(canvas, bg=BG_COLOR)
    inner_frame_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(inner_frame_id, width=event.width)

    canvas.bind('<Configure>', on_canvas_configure)

    # 交通信息框架
    traffic_frame = tk.LabelFrame(inner_frame, text="交通", font=('Arial', 13, 'bold'), fg='white', bg=PRIMARY_COLOR, bd=0, relief=tk.FLAT, padx=15, pady=10, labelanchor='n')
    traffic_frame.pack(pady=(0, 5), padx=0, fill=tk.X)

    traffic_options = [
        ("高铁：", train_link, 'train'), # 添加图标键 'train'
        ("航班：", air_link, 'airplane'),   # 添加图标键 'airplane'
    ]
    for idx, (label_text, link, icon_key) in enumerate(traffic_options): # 修改循环以解包图标键
        # 创建带图标的标签
        icon_label = tk.Label(traffic_frame, text=label_text, image=icon_images.get(icon_key), compound='left', font=('Arial', 15), bg=PRIMARY_COLOR, fg='white')
        icon_label.image = icon_images.get(icon_key) # 保持对图片的引用
        icon_label.grid(row=idx, column=0, padx=(60,0), pady=5, sticky='w') # Increased left padding
        # 检查链接是否存在且不为空
        if link:
            link_label = tk.Label(traffic_frame, text="订票链接点这里哦", font=('Arial', 12), fg='white', cursor='hand2', bg=PRIMARY_COLOR)
            link_label.bind("<Button-1>", lambda e, url=link: webbrowser.open(url)) # Bind click event
            link_label.grid(row=idx, column=1, padx=(0,100), pady=5, sticky='w')
        else:
            # 如果没有链接，可以显示不同文本或禁用按钮
            tk.Label(traffic_frame, text="无链接", font=('Arial', 11), fg='grey', bg=PRIMARY_COLOR).grid(row=idx, column=1, padx=(0,20), pady=5, sticky='w')

    # 定义类别和对应的图标键及文本
    category_definitions = [
        ('weather', '天气'),
        ('play', '游玩'),
        ('food', '餐饮'),
        ('lodging', '住宿')
    ]

    # 使用传入的天数参数
    try:
        int_days = int(days)
    except ValueError:
        int_days = 3  # 如果转换失败，默认显示3天
    
    for i in range(1, int_days + 1): # 使用传入的天数
        tk.Label(inner_frame, text=f"Day {i}", font=('Arial', 14, 'bold'), bg=PRIMARY_COLOR, fg='white').pack(pady=(0, 5), padx=10, fill=tk.X) # Reduced top padding
        table_frame = tk.Frame(inner_frame, bg=BG_COLOR)
        table_frame.pack(pady=20)

        # Configure columns for alignment across days
        table_frame.grid_columnconfigure(0, minsize=230) # Min width for Icon/Label col (approx width=150 + padx=60+20)
        table_frame.grid_columnconfigure(1, weight=1)    # Allow Content col to expand
        table_frame.grid_columnconfigure(2, minsize=100) # Min width for Link col
        
        for idx, (icon_key, text) in enumerate(category_definitions):
            # Icon + Category Text Label
            icon_label = tk.Label(table_frame, image=icon_images.get(icon_key), text=text, compound='left', font=('Arial', 12, 'bold'), width=150, anchor="w", bg=BG_COLOR, fg='black')
            icon_label.image = icon_images.get(icon_key) # 保持对图片的引用
            icon_label.grid(row=idx, column=0, padx=(60, 20), pady=5, sticky='w') # Adjusted grid

            # Determine Content Text and Link URL
            content_text = "信息待获取" # 默认文本
            link_url = None
            link_display_text = "查看链接" # Text for the link
            current_day_index = i - 1 # 列表索引从0开始

            try:
                if icon_key == 'weather':
                    content_text = "天气信息待接入"
                elif icon_key == 'play':
                    # Ensure spot_list has data for the day
                    content_text = spot_list[current_day_index].strip() if current_day_index < len(spot_list) and spot_list[current_day_index] else "自由活动"
                elif icon_key == 'food':
                    # Ensure restaurant_list and link_list have data for the day
                    if current_day_index < len(restaurant_list) and restaurant_list[current_day_index]:
                        content_text = restaurant_list[current_day_index]
                        if current_day_index < len(restaurant_link_list) and restaurant_link_list[current_day_index]:
                            link_url = restaurant_link_list[current_day_index]
                    else:
                        content_text = "自寻美食"
                elif icon_key == 'lodging':
                    # Ensure hotel_list and link_list have data for the day, with fallback
                    if current_day_index < len(hotel_list) and hotel_list[current_day_index]:
                        content_text = hotel_list[current_day_index]
                        if current_day_index < len(hotel_link_list) and hotel_link_list[current_day_index]:
                            link_url = hotel_link_list[current_day_index]
                    elif len(hotel_list) > 2 and hotel_list[2]: # Fallback to day 3 (index 2) if current day empty and day 3 exists
                         content_text = hotel_list[2]
                         if 2 < len(hotel_link_list) and hotel_link_list[2]: # Check link for fallback
                             link_url = hotel_link_list[2]
                    else:
                         content_text = "未指定住宿" # Default if no data

            except IndexError:
                # This handles cases where lists (spot_list, restaurant_list, etc.) are shorter than expected
                content_text = "信息缺失"

            # Content Text Label
            content_label = tk.Label(table_frame, text=content_text, anchor="w", bg=BG_COLOR, fg='black', wraplength=450, justify=tk.LEFT) # Reduced wraplength for narrower column
            content_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')

            # Clickable Link Label (only for food/lodging with a valid link)
            if link_url and isinstance(link_url, str) and link_url.strip() and (icon_key == 'food' or icon_key == 'lodging'):
                link_widget = tk.Label(table_frame, text=link_display_text, font=('Arial', 11), fg='lightblue', cursor='hand2', bg=BG_COLOR)
                # Ensure lambda captures the correct URL for this iteration
                link_widget.bind("<Button-1>", lambda e, url=link_url: webbrowser.open(url))
                link_widget.grid(row=idx, column=2, padx=10, pady=5, sticky='w')

    # Pack scrollbar and canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    class HamsterChatWindow:
        def __init__(self, master):
            self.window = tk.Toplevel(master)
            self.window.title("小仓鼠聊天助手")
            self.window.geometry("700x600")
            self.window.configure(bg=BG_COLOR)

            # 聊天记录区域
            self.chat_frame = tk.Frame(self.window, bg=BG_COLOR)
            self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.chat_canvas = tk.Canvas(self.chat_frame, bg=BG_COLOR)
            self.chat_scrollbar = tk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_canvas.yview)
            self.chat_container = tk.Frame(self.chat_canvas, bg=BG_COLOR)

            self.chat_container.bind('<Configure>', lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox('all')))
            self.chat_canvas.create_window((0, 0), window=self.chat_container, anchor='nw')
            self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

            self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # 输入区域
            self.input_frame = tk.Frame(self.window, bg=BG_COLOR)
            self.input_frame.pack(fill=tk.X, padx=10, pady=10)

            self.input_entry = tk.Entry(self.input_frame, width=50, font=('Arial', 12))
            self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

            self.send_button = CapsuleButton(self.input_frame, text="发送", command=self.send_message, bg=PRIMARY_COLOR, fg="white")
            self.send_button.pack(side=tk.RIGHT)

            # 绑定回车键发送消息
            self.input_entry.bind('<Return>', lambda event: self.send_message())

            # 对话历史
            self.messages = []
            self.client = None

        def create_message_label(self, message, is_user=True):
            frame = tk.Frame(self.chat_container, bg=BG_COLOR)
            if is_user:
                frame.pack(fill=tk.X, pady=5, anchor='e')  # 用户消息靠右
            else:
                frame.pack(fill=tk.X, pady=5, anchor='w')  # AI消息靠左

            radius = 36  # 圆角更大
            padding_x = 20
            padding_y = 14
            font = ('Arial', 11)
            max_width = 600

            # 计算多行文本尺寸（自动换行）
            font_obj = tkFont.Font(font=font)
            words = message.split(' ')
            lines = []
            current_line = ''
            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                if font_obj.measure(test_line) > max_width:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
            text_height = font_obj.metrics('linespace') * len(lines)
            text_width = min(max([font_obj.measure(line) for line in lines] + [0]), max_width)

            bubble_width = text_width + 2 * padding_x
            bubble_height = text_height + 2 * padding_y

            # AI回复为主题蓝色
            from travel_hamster_utils import PRIMARY_COLOR
            bg_color = (255, 255, 255, 255) if is_user else tuple(int(PRIMARY_COLOR.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            # 阴影
            shadow_offset = 2
            shadow_color = (180, 180, 180, 80)
            bubble_img = Image.new('RGBA', (bubble_width, bubble_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(bubble_img)
            draw.rounded_rectangle([
                shadow_offset, shadow_offset, bubble_width, bubble_height
            ], radius=radius, fill=shadow_color)
            draw.rounded_rectangle([
                0, 0, bubble_width - shadow_offset, bubble_height - shadow_offset
            ], radius=radius, fill=bg_color)
            bubble_tk = ImageTk.PhotoImage(bubble_img)
            canvas = tk.Canvas(frame, width=bubble_width, height=bubble_height, bg=BG_COLOR, highlightthickness=0, bd=0)
            canvas.create_image(0, 0, anchor='nw', image=bubble_tk)
            canvas.image = bubble_tk
            canvas.pack(side='right' if is_user else 'left', padx=10)
            # 自动换行并自适应宽高
            import textwrap
            max_width = 600
            font_obj = tkFont.Font(font=font)
            # 先按字符宽度分行
            wrapped_lines = []
            for paragraph in message.split('\n'):
                line = ''
                for char in paragraph:
                    test_line = line + char
                    if font_obj.measure(test_line) > max_width - 20:
                        if line:
                            wrapped_lines.append(line)
                        line = char
                    else:
                        line = test_line
                if line:
                    wrapped_lines.append(line)
            text_width = min(max([font_obj.measure(line) for line in wrapped_lines]+[0]), max_width)
            text_height = font_obj.metrics('linespace') * len(wrapped_lines)
            bubble_width = text_width + 2 * padding_x
            bubble_height = text_height + 2 * padding_y

            # 重新生成圆角气泡背景
            bubble_img = Image.new('RGBA', (bubble_width, bubble_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(bubble_img)
            from travel_hamster_utils import PRIMARY_COLOR
            bg_color = (255,255,255,255) if is_user else tuple(int(PRIMARY_COLOR.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            shadow_offset = 2
            shadow_color = (180, 180, 180, 80)
            draw.rounded_rectangle([
                shadow_offset, shadow_offset, bubble_width, bubble_height
            ], radius=radius, fill=shadow_color)
            draw.rounded_rectangle([
                0, 0, bubble_width - shadow_offset, bubble_height - shadow_offset
            ], radius=radius, fill=bg_color)
            bubble_tk = ImageTk.PhotoImage(bubble_img)
            canvas.config(width=bubble_width, height=bubble_height)
            canvas.create_image(0, 0, anchor='nw', image=bubble_tk)
            canvas.image = bubble_tk
            # 重新绘制文字
            y = padding_y
            text_color = 'black' if is_user else 'white'
            for line in wrapped_lines:
                canvas.create_text(padding_x, y, anchor='nw', text=line, font=font, fill=text_color)
                y += font_obj.metrics('linespace')

        def send_message(self):
            user_input = self.input_entry.get().strip()
            if not user_input:
                return

            # 清空输入框
            self.input_entry.delete(0, tk.END)

            # 显示用户消息
            self.create_message_label(user_input, is_user=True)
            self.messages.append({"role": "user", "content": user_input})

            # 初始化 OpenAI 客户端
            if not self.client:
                import os
                from dotenv import load_dotenv
                load_dotenv()
                self.client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

            try:
                # 发送对话请求
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个可爱的旅行小仓鼠助手，擅长提供旅行建议和有趣的旅行小知识"},
                        *self.messages
                    ],
                    stream=False
                )
                
                # 获取并显示小仓鼠回复
                hamster_reply = response.choices[0].message.content
                self.create_message_label(hamster_reply, is_user=False)
                self.messages.append({"role": "assistant", "content": hamster_reply})

                # 自动滚动到底部
                self.chat_canvas.yview_moveto(1.0)

            except Exception as e:
                error_msg = f"对话出现问题：{str(e)}"
                self.create_message_label(error_msg, is_user=False)

    def open_hamster_chat():
        HamsterChatWindow(root)

    # 添加与小仓鼠对话的按钮
    chat_button = CapsuleButton(top_frame, text="与小仓鼠对话", command=open_hamster_chat, bg=PRIMARY_COLOR, fg="white")
    chat_button.pack(side='right', padx=20, pady=10)
