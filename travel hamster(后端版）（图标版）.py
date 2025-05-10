import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import time
import os

# 颜色主题
PRIMARY_COLOR = '#6EC6F2'  # 主色调淡蓝
BG_COLOR = '#F6FBFF'       # 背景色
ENTRY_BG = '#FFFFFF'       # 输入框背景
BUTTON_BG = '#6EC6F2'      # 按钮背景
BUTTON_ACTIVE = '#3B8EB5'  # 按钮按下
LABEL_COLOR = '#333333'    # 文字颜色

# 图标路径
ICON_DIR = './icongif'

# 图标文件名映射
ICON_MAP = {
    'title': 'title.gif',           # 标题
    'start': 'start.gif',           # 出发地
    'destination': 'destination.gif', # 目的地
    'date': 'date.gif',             # 出发日期
    'days': 'days.gif',             # 旅行天数
    'purpose': 'purpose.gif',       # 旅行目的
    'wanted': 'wanted.gif',         # 特别想去的地方
    'people': 'people.gif',         # 出行人数
    'other': 'other.gif',           # 其他想说的话
}

# 统一加载所有图标，防止被垃圾回收
icon_images = {}
def load_icons():
    try:
        from PIL import Image, ImageTk
        PIL_OK = True
    except ImportError:
        PIL_OK = False
        print('[图标加载] 未安装 Pillow，图片将不自动缩放。建议 pip install pillow')
    target_height = 44  # 两行文字高度
    for key, fname in ICON_MAP.items():
        full_path = f"{ICON_DIR}/{fname}"
        if not os.path.exists(full_path):
            print(f"[图标加载] 文件不存在: {full_path}")
            icon_images[key] = None
            continue
        try:
            if PIL_OK:
                img = Image.open(full_path)
                w, h = img.size
                if h != target_height:
                    scale = target_height / h
                    new_w = int(w * scale)
                    img = img.resize((new_w, target_height), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                icon_images[key] = tk_img
                print(f"[图标加载] 成功并缩放: {full_path} -> {new_w}x{target_height}")
            else:
                tk_img = tk.PhotoImage(file=full_path)
                icon_images[key] = tk_img
                print(f"[图标加载] 成功: {full_path}")
        except Exception as e:
            print(f"[图标加载] 失败: {full_path}, 错误: {e}")
            icon_images[key] = None

# 自定义圆角胶囊按钮（带动画）
class CapsuleButton(tk.Canvas):
    def __init__(self, master, text, command=None, width=180, height=48, radius=24, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=master['bg'], bd=0)
        self.radius = radius
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.bg = BUTTON_BG
        self.fg = 'white'
        self.active_bg = BUTTON_ACTIVE
        self.current_bg = self.bg
        self.text_id = None
        self.rect_id = None
        self.animating = False
        self.draw_button(self.bg)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.text_item = self.create_text(self.width//2, self.height//2, text=self.text, font=('Arial', 15, 'bold'), fill=self.fg)

    def draw_button(self, color):
        self.delete('capsule')
        r = self.radius
        w = self.width
        h = self.height
        # 画一个圆角矩形
        self.create_oval(0, 0, 2*r, h, fill=color, outline=color, tags='capsule')
        self.create_oval(w-2*r, 0, w, h, fill=color, outline=color, tags='capsule')
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color, tags='capsule')

    def animate_to(self, target_color, steps=8, interval=18):
        if self.animating:
            return
        self.animating = True
        start_color = self.current_bg
        start_rgb = self.winfo_rgb(start_color)
        end_rgb = self.winfo_rgb(target_color)
        dr = (end_rgb[0] - start_rgb[0]) // steps
        dg = (end_rgb[1] - start_rgb[1]) // steps
        db = (end_rgb[2] - start_rgb[2]) // steps
        def step(i=1, r=start_rgb[0], g=start_rgb[1], b=start_rgb[2]):
            if i > steps:
                self.current_bg = target_color
                self.draw_button(target_color)
                self.animating = False
                return
            nr = r + dr
            ng = g + dg
            nb = b + db
            hex_color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
            self.draw_button(hex_color)
            self.after(interval, lambda: step(i+1, nr, ng, nb))
        step()

    def on_click(self, event):
        self.animate_to(self.active_bg, steps=5, interval=10)
    def on_release(self, event):
        self.animate_to(self.bg)
        if self.command:
            self.command()

# 自定义圆角胶囊输入框
class CapsuleEntry(tk.Frame):
    def __init__(self, master, width=260, height=38, radius=19, font=('Arial', 12), **kwargs):
        super().__init__(master, bg=master['bg'])
        self.width = width
        self.height = height
        self.radius = radius
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg=master['bg'], bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_capsule()
        self.entry = tk.Entry(self, font=font, bd=0, relief='flat', bg=ENTRY_BG, fg=LABEL_COLOR, highlightthickness=0, borderwidth=0, insertbackground=LABEL_COLOR, **kwargs)
        self.entry.place(x=radius, y=6, width=width-2*radius, height=height-12)
    def draw_capsule(self):
        r = self.radius
        w = self.width
        h = self.height
        self.canvas.create_oval(0, 0, 2*r, h, fill=ENTRY_BG, outline=ENTRY_BG)
        self.canvas.create_oval(w-2*r, 0, w, h, fill=ENTRY_BG, outline=ENTRY_BG)
        self.canvas.create_rectangle(r, 0, w-r, h, fill=ENTRY_BG, outline=ENTRY_BG)
    def get(self):
        return self.entry.get()
    def insert(self, idx, val):
        self.entry.insert(idx, val)
    def delete(self, start, end=None):
        self.entry.delete(start, end)
    def bind(self, *args, **kwargs):
        self.entry.bind(*args, **kwargs)

# 鼠标悬停变色功能（ttk.Button 用 style.map 实现，无需事件绑定）
def on_enter(e):
    pass

def on_leave(e):
    pass

def get_selected_options():
    return [options[i] for i, var in enumerate(option_vars) if var.get() == 1]

def validate_input():
    fields = {
        startanswer: "出发地",
        destinationanswer: "目的地",
        dateyearanswer: "出发年份",
        datemonthanswer: "出发月份",
        dateanswer: "出发日期",
        sumdayanswer: "旅行天数",
        wantedanswer: "特别想去的地方（没有的话请告诉小仓鼠随便安排哦",
        peopleanswer: "出行人数",
        exanswer: "小仓鼠想知道你还有什么想对小仓鼠说的话づ♡ど"
    }
    for entry, field_name in fields.items():
        if not entry.get():
            messagebox.showwarning("提示", f"请输入{field_name}")
            return False
    target = get_selected_options()
    if not target:
        messagebox.showwarning("提示", "请至少选择一个选项。")
        return False
    return True

def save_info():
    startplace = startanswer.get()
    destination = destinationanswer.get()
    startyear = dateyearanswer.get()
    startmonth = datemonthanswer.get()
    startdate = dateanswer.get()
    days = sumdayanswer.get()
    wanttogo = wantedanswer.get()
    people = peopleanswer.get()
    other = exanswer.get()
    target = get_selected_options()

    with open('inputinfo.txt', 'a', encoding='utf-8') as f:
        f.write(f"出发地: {startplace}\n 目的地：{destination}\n出发时间：{startyear, startmonth, startdate}\n"
                f"旅行天数：{days}\n旅行目的: {', '.join(target)}\n特别想去的地方：{wanttogo}\n"
                f"出行人数：{people}\n其他的话：{other}\n")

def show_next_window():
    root.withdraw()
    new_window = tk.Toplevel(root)
    new_window.title("下一个界面")
    tk.Label(new_window, text="小仓鼠已成功收集信息，欢迎进入下一个界面！").pack(pady=50)

    def next_window():
        new_window.destroy()
        window2 = tk.Toplevel(root)
        window2.title("travel hamster")
        window2.geometry("1000x650+250+100")

        top_frame = tk.Frame(window2)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Welcome to travel hamster~!", font=('Arial', 16), width=1000, height=3,
                 bg='lightblue').pack()
        tk.Label(top_frame, text="").pack()
        tk.Label(top_frame, text="铛铛！以下是小仓鼠为你准备的旅行攻略~", font=('Arial', 12, 'bold')).pack()
        tk.Label(top_frame, text="💙请查收₍ᐢ..ᐢ₎♡", font=('Arial', 12, 'bold')).pack()

        frame = tk.Frame(window2)
        frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        try:
            num_days = int(sumdayanswer.get())
            for i in range(1, num_days + 1):
                tk.Label(inner_frame, text=f"Day {i}", font=('Arial', 14, 'bold')).pack(pady=20)

                table_frame = tk.Frame(inner_frame)
                table_frame.pack(pady=20)

                categories = ["天气", "游玩", "餐饮", "住宿"]
                try:
                    response = requests.get('http://127.0.0.1:5000/get_travel_info')
                    if response.status_code == 200:
                        travel_info = response.json()
                        for idx, category in enumerate(categories):
                            tk.Label(table_frame, text=category, font=('Arial', 12, 'bold'), width=10,
                                     anchor="w").grid(row=idx * 3, column=1, padx=60, pady=10, rowspan=3)

                            content = travel_info.get(category, "待安排")
                            tk.Label(table_frame, text=content, width=100, anchor="w").grid(
                                row=idx * 3, column=2, columnspan=10, padx=10, pady=10, rowspan=3)
                    else:
                        messagebox.showerror("错误", f"请求失败，状态码：{response.status_code}")
                except requests.RequestException as e:
                    messagebox.showerror("错误", f"请求出错：{e}")

        except ValueError:
            messagebox.showerror("错误", "输入的旅行天数不是有效的整数。")

    ttk.Button(new_window, text="确认", command=next_window, style='Capsule.TButton').pack()

def collect_and_next():
    if validate_input():
        save_info()
        show_next_window()

root = tk.Tk()
root.title("travel hamster")
root.geometry("1000x650+250+100")
root.configure(bg=BG_COLOR)
load_icons()

# 标题区（居中）
header_frame = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
header_frame.pack(fill=tk.X)

# 居中容器（用于图标+标题整体居中）
center_header = tk.Frame(header_frame, bg=PRIMARY_COLOR)
center_header.place(relx=0.5, rely=0.5, anchor='center')

# 让标题图标高度约等于两行标题文字
TITLE_FONT_SIZE = 24
TITLE_ICON_HEIGHT = int(TITLE_FONT_SIZE * 2 * 1.1)  # 2行字高，略加间距
if icon_images.get('title'):
    try:
        from PIL import Image, ImageTk
        orig_path = f"{ICON_DIR}/{ICON_MAP['title']}"
        img = Image.open(orig_path)
        w, h = img.size
        scale = TITLE_ICON_HEIGHT / h
        new_size = (int(w * scale), TITLE_ICON_HEIGHT)
        img = img.resize(new_size, Image.LANCZOS)
        title_img_big = ImageTk.PhotoImage(img)
        icon_label = tk.Label(center_header, image=title_img_big, bg=PRIMARY_COLOR)
        icon_label.image = title_img_big
        icon_label.pack(side=tk.LEFT, padx=(0, 30), pady=10)
    except Exception as e:
        icon_label = tk.Label(center_header, image=icon_images['title'], bg=PRIMARY_COLOR)
        icon_label.image = icon_images['title']
        icon_label.pack(side=tk.LEFT, padx=(0, 30), pady=10)
else:
    icon_label = tk.Label(center_header, text="🐹", font=('Arial', TITLE_FONT_SIZE * 2), bg=PRIMARY_COLOR)
    icon_label.pack(side=tk.LEFT, padx=(0, 30), pady=10)

main_title = tk.Label(center_header, text="Welcome to travel hamster~!", font=('Arial', TITLE_FONT_SIZE, 'bold'), bg=PRIMARY_COLOR, fg='white')
main_title.pack(side=tk.LEFT, pady=10)

# 简介区
intro_frame = tk.Frame(root, bg=BG_COLOR)
intro_frame.pack(fill=tk.X, pady=(10, 0))
intro_label = tk.Label(intro_frame, text="💙欢迎光临旅行仓鼠的小屋~这里你可以通过告诉小仓鼠你的需求从而获得小仓鼠为你私人化定制的旅行计划₍ᐢ..ᐢ₎♡", font=('Arial', 12, 'bold'), bg=BG_COLOR, fg=LABEL_COLOR, anchor='center', justify='center')
intro_label.pack(padx=20, pady=10)

# 表单区
form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(pady=(10, 0))

# --- 出发地 ---
row0 = tk.Frame(form_frame, bg=BG_COLOR)
row0.pack(fill='x', pady=4)
if icon_images['start']:
    tk.Label(row0, image=icon_images['start'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row0, text="出发地：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left')
startanswer = CapsuleEntry(row0)
startanswer.pack(side='left', padx=(6, 0))

# --- 目的地 ---
row1 = tk.Frame(form_frame, bg=BG_COLOR)
row1.pack(fill='x', pady=4)
if icon_images['destination']:
    tk.Label(row1, image=icon_images['destination'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row1, text="目的地：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left')
destinationanswer = CapsuleEntry(row1)
destinationanswer.pack(side='left', padx=(6, 0))

# --- 出发日期 ---
row2 = tk.Frame(form_frame, bg=BG_COLOR)
row2.pack(fill='x', pady=4)
if icon_images['date']:
    tk.Label(row2, image=icon_images['date'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row2, text="出发日期：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left')
entry_width = 60
tight_padx = 2
dateyearanswer = CapsuleEntry(row2, width=entry_width)
dateyearanswer.pack(side='left', padx=(0, 0))
tk.Label(row2, text='年', font=('Arial', 12), bg=BG_COLOR).pack(side='left', padx=(tight_padx, 0))
datemonthanswer = CapsuleEntry(row2, width=entry_width)
datemonthanswer.pack(side='left', padx=(tight_padx, 0))
tk.Label(row2, text="月", font=('Arial', 12), bg=BG_COLOR).pack(side='left', padx=(tight_padx, 0))
dateanswer = CapsuleEntry(row2, width=entry_width)
dateanswer.pack(side='left', padx=(tight_padx, 0))
tk.Label(row2, text="日", font=('Arial', 12), bg=BG_COLOR).pack(side='left', padx=(tight_padx, 0))

# --- 旅行天数 ---
row3 = tk.Frame(form_frame, bg=BG_COLOR)
row3.pack(fill='x', pady=4)
if icon_images['days']:
    tk.Label(row3, image=icon_images['days'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row3, text="旅行天数：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left')
sumdayanswer = CapsuleEntry(row3, width=60)
sumdayanswer.pack(side='left', padx=(6, 0))
tk.Label(row3, text="天", font=('Arial', 12), bg=BG_COLOR).pack(side='left', padx=(2, 0))

# --- 旅行目的 2x2 ---
row4 = tk.Frame(form_frame, bg=BG_COLOR)
row4.pack(fill='x', pady=4)
if icon_images['purpose']:
    tk.Label(row4, image=icon_images['purpose'], bg=BG_COLOR).pack(side='left', padx=(0, 4), anchor='n')
purpose_label = tk.Label(row4, text="旅行目的：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR)
purpose_label.pack(side='left', anchor='n', pady=2)
options = ["风景", "美食", "玩乐", "旅拍"]
option_vars = []
cb_frame = tk.Frame(row4, bg=BG_COLOR)
cb_frame.pack(side='left', padx=(10, 0))
for i, option in enumerate(options):
    var = tk.IntVar()
    option_vars.append(var)
    cb = tk.Checkbutton(cb_frame, text=option, variable=var, font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR, selectcolor=PRIMARY_COLOR, activebackground=BG_COLOR, activeforeground=PRIMARY_COLOR)
    r, c = divmod(i, 2)
    cb.grid(row=r, column=c, padx=8, pady=2, sticky='w')

# --- 特别想去的地方 ---
row5 = tk.Frame(form_frame, bg=BG_COLOR)
row5.pack(fill='x', pady=4)
if icon_images['wanted']:
    tk.Label(row5, image=icon_images['wanted'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row5, text="特别想去的地方:", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left')
wantedanswer = CapsuleEntry(row5)
wantedanswer.pack(side='left', padx=(6, 0))

# --- 出行人数 ---
row6 = tk.Frame(form_frame, bg=BG_COLOR)
row6.pack(fill='x', pady=4)
if icon_images['people']:
    tk.Label(row6, image=icon_images['people'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row6, text="出行人数：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left')
peopleanswer = CapsuleEntry(row6, width=60)
peopleanswer.pack(side='left', padx=(6, 0))

# --- 其他想说的话（独立一行） ---
row7 = tk.Frame(form_frame, bg=BG_COLOR)
row7.pack(fill='x', pady=4)
if icon_images['other']:
    tk.Label(row7, image=icon_images['other'], bg=BG_COLOR).pack(side='left', padx=(0, 4), anchor='n')
tk.Label(row7, text="还有其他想对小仓鼠说的话吗⌯'▾'⌯：", font=('Arial', 12), bg=BG_COLOR, fg=LABEL_COLOR).pack(side='left', anchor='n', pady=2)
exanswer = CapsuleEntry(row7, width=340)
exanswer.pack(side='left', padx=(6, 0), fill='x', expand=True)

# 按钮区
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=30)

submit_btn = CapsuleButton(button_frame, text="完成！", command=collect_and_next)
submit_btn.pack()

root.mainloop()
