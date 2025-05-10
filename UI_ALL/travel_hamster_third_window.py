import tkinter as tk
from tkinter import ttk # Import ttk
from tkinter import messagebox
from travel_hamster_utils import CapsuleButton, BG_COLOR, PRIMARY_COLOR, icon_images, load_icons

def show_third_window(root):
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

    # 定义类别和对应的图标键及文本
    category_definitions = [
        ('weather', '天气'),
        ('play', '游玩'),
        ('food', '餐饮'),
        ('lodging', '住宿')
    ]

    for i in range(1, 4): # 假设显示3天
        tk.Label(inner_frame, text=f"Day {i}", font=('Arial', 14, 'bold'), bg=PRIMARY_COLOR, fg='white').pack(pady=(20, 5), padx=10, fill=tk.X)
        table_frame = tk.Frame(inner_frame, bg=BG_COLOR)
        table_frame.pack(pady=20)
        
        for idx, (icon_key, text) in enumerate(category_definitions):
            icon_label = tk.Label(table_frame, image=icon_images.get(icon_key), text=text, compound='left', font=('Arial', 12, 'bold'), width=150, anchor="w", bg=BG_COLOR, fg='black')
            icon_label.image = icon_images.get(icon_key) # 保持对图片的引用
            icon_label.grid(row=idx * 3, column=1, padx=60, pady=10, rowspan=3, sticky='w')
            tk.Label(table_frame, text="待安排", width=100, anchor="w", bg=BG_COLOR, fg='black').grid(row=idx * 3, column=2, columnspan=10, padx=10, pady=10, rowspan=3, sticky='w')

    # Pack scrollbar and canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
