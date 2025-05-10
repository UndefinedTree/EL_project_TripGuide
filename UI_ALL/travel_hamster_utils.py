import tkinter as tk
from tkinter import ttk
import os
PRIMARY_COLOR = '#6EC6F2'  # 主色调淡蓝
BG_COLOR = '#F6FBFF'       # 背景色
ENTRY_BG = '#FFFFFF'       # 输入框背景
BUTTON_BG = '#6EC6F2'      # 按钮背景
BUTTON_ACTIVE = '#3B8EB5'  # 按钮按下
LABEL_COLOR = '#333333'    # 文字颜色
ICON_DIR = '/Users/wangxizheng/MINE/MyProject/EL_project_TripGuide/icongif'
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
    'weather': 'weather.gif',       # 天气
    'play': 'goout.gif',            # 游玩
    'food': 'food.gif',             # 餐饮
    'lodging': 'hotel.gif',         # 住宿
}
icon_images = {}
def load_icons():
    try:
        from PIL import Image, ImageTk
        PIL_OK = True
    except ImportError:
        PIL_OK = False
        print('[图标加载] 未安装 Pillow，图片将不自动缩放。建议 pip install pillow')
    target_height = 44
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
                else:
                    new_w = w
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
        self.create_oval(0, 0, 2*r, h, fill=color, outline=color, tags='capsule')
        self.create_oval(w-2*r, 0, w, h, fill=color, outline=color, tags='capsule')
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color, tags='capsule')
    def animate_to(self, target_color, steps=8, interval=18):
        pass
    def on_click(self, event):
        self.itemconfig(self.text_item, text=self.text)
        self.update_idletasks()
    def on_release(self, event):
        self.itemconfig(self.text_item, text=self.text)
        self.update_idletasks()
        if self.command:
            self.command()
class CapsuleEntry(tk.Frame):
    def __init__(self, master, width=260, height=38, radius=19, font=('Arial', 12), placeholder='', **kwargs):
        super().__init__(master, bg=master['bg'])
        self.width = width
        self.height = height
        self.radius = radius
        self.placeholder = placeholder
        self.font = font
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg=master['bg'], bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_capsule()
        self.entry = tk.Entry(self, font=font, bd=0, relief='flat', bg=ENTRY_BG, fg=LABEL_COLOR, highlightthickness=0, borderwidth=0, insertbackground=LABEL_COLOR, **kwargs)
        self.entry.place(x=radius, y=6, width=width-2*radius, height=height-12)
        self.placeholder_color = '#bbbbbb'
        self.default_fg = LABEL_COLOR
        if placeholder:
            self.set_placeholder()
            self.entry.bind('<FocusIn>', self.clear_placeholder)
            self.entry.bind('<FocusOut>', self.set_placeholder)
    def draw_capsule(self):
        r = self.radius
        w = self.width
        h = self.height
        self.canvas.create_oval(0, 0, 2*r, h, fill=ENTRY_BG, outline=ENTRY_BG)
        self.canvas.create_oval(w-2*r, 0, w, h, fill=ENTRY_BG, outline=ENTRY_BG)
        self.canvas.create_rectangle(r, 0, w-r, h, fill=ENTRY_BG, outline=ENTRY_BG)
    def set_placeholder(self, event=None):
        if not self.entry.get():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.placeholder_color)
    def clear_placeholder(self, event=None):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.default_fg)
    def get(self):
        val = self.entry.get()
        if self.placeholder and val == self.placeholder:
            return ''
        return val
    def insert(self, idx, val):
        self.clear_placeholder()
        self.entry.insert(idx, val)
    def delete(self, start, end=None):
        self.entry.delete(start, end)
    def bind(self, *args, **kwargs):
        self.entry.bind(*args, **kwargs)
