import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from travel_hamster_utils import CapsuleButton, CapsuleEntry, load_icons, PRIMARY_COLOR, BG_COLOR, ENTRY_BG, BUTTON_BG, BUTTON_ACTIVE, LABEL_COLOR, ICON_DIR, ICON_MAP, icon_images

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
        if entry == exanswer:  # 如果是 exanswer 字段
            continue          # 则跳过必填检查
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

def collect_and_next():
    if validate_input():
        save_info()
        show_next_window()

def show_next_window():
    import travel_hamster_second_window
    root.withdraw()
    travel_hamster_second_window.show_second_window(root)

# 主窗口
root = tk.Tk()
root.title("travel hamster")
root.geometry("1200x700+250+100")
root.configure(bg=BG_COLOR)
load_icons()

# 标题区（居中）
header_frame = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
header_frame.pack(fill=tk.X)

center_header = tk.Frame(header_frame, bg=PRIMARY_COLOR)
center_header.place(relx=0.5, rely=0.5, anchor='center')

TITLE_FONT_SIZE = 24
TITLE_ICON_HEIGHT = int(TITLE_FONT_SIZE * 2 * 1.1)
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
intro_label = tk.Label(intro_frame, text="💙欢迎光临旅行仓鼠的小屋~这里你可以通过告诉小仓鼠你的需求从而获得小仓鼠为你私人化定制的旅行计划₍ᐢ..ᐢ₎♡", font=('Arial', 12, 'bold'), bg=BG_COLOR, fg='black', anchor='center', justify='center')
intro_label.pack(padx=20, pady=10)

# 表单区
form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(pady=(10, 0))

# --- 出发地 ---
row0 = tk.Frame(form_frame, bg=BG_COLOR)
row0.pack(fill='x', pady=4)
if icon_images['start']:
    tk.Label(row0, image=icon_images['start'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row0, text="出发地：", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
global startanswer
startanswer = CapsuleEntry(row0, placeholder='请输入出发地')
startanswer.pack(side='left', padx=(6, 0))

# --- 目的地 ---
row1 = tk.Frame(form_frame, bg=BG_COLOR)
row1.pack(fill='x', pady=4)
if icon_images['destination']:
    tk.Label(row1, image=icon_images['destination'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row1, text="目的地：", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
global destinationanswer
destinationanswer = CapsuleEntry(row1, placeholder='请输入目的地')
destinationanswer.pack(side='left', padx=(6, 0))

# --- 出发日期 ---
row2 = tk.Frame(form_frame, bg=BG_COLOR)
row2.pack(fill='x', pady=4)
if icon_images['date']:
    tk.Label(row2, image=icon_images['date'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row2, text="出发日期：", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
entry_width = 120  # 宽度加倍

global dateyearanswer, datemonthanswer, dateanswer

tight_padx = 2
dateyearanswer = CapsuleEntry(row2, width=entry_width, placeholder='如2025')
dateyearanswer.pack(side='left', padx=(0, 0))
tk.Label(row2, text='年', font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left', padx=(tight_padx, 0))
datemonthanswer = CapsuleEntry(row2, width=entry_width, placeholder='如5')
datemonthanswer.pack(side='left', padx=(tight_padx, 0))
tk.Label(row2, text="月", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left', padx=(tight_padx, 0))
dateanswer = CapsuleEntry(row2, width=entry_width, placeholder='如10')
dateanswer.pack(side='left', padx=(tight_padx, 0))
tk.Label(row2, text="日", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left', padx=(tight_padx, 0))

# --- 旅行天数 ---
row3 = tk.Frame(form_frame, bg=BG_COLOR)
row3.pack(fill='x', pady=4)
if icon_images['days']:
    tk.Label(row3, image=icon_images['days'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
tk.Label(row3, text="旅行天数：", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
global sumdayanswer
sumdayanswer = CapsuleEntry(row3, width=60, placeholder='如3')
sumdayanswer.pack(side='left', padx=(6, 0))
tk.Label(row3, text="天", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left', padx=(2, 0))

# --- 旅行目的 2x2 ---
row4 = tk.Frame(form_frame, bg=BG_COLOR)
row4.pack(fill='x', pady=4)
if icon_images['purpose']:
    tk.Label(row4, image=icon_images['purpose'], bg=BG_COLOR).pack(side='left', padx=(0, 4), anchor='n')
purpose_label = tk.Label(row4, text="旅行目的：", font=('Arial', 12), bg=BG_COLOR, fg='black')
purpose_label.pack(side='left', anchor='n', pady=2)
global options, option_vars
options = ["风景", "美食", "玩乐", "旅拍"]
option_vars = []
cb_frame = tk.Frame(row4, bg=BG_COLOR)
cb_frame.pack(side='left', padx=(6, 0))
for i, option in enumerate(options):
    var = tk.IntVar()
    option_vars.append(var)
    tk.Checkbutton(cb_frame, text=option, variable=var, font=('Arial', 12), bg=BG_COLOR, fg='black', selectcolor=BG_COLOR, activeforeground='black').pack(side='left', padx=8)

# --- 特别想去的地方 ---
row5 = tk.Frame(form_frame, bg=BG_COLOR)
row5.pack(fill='x', pady=4)
if icon_images['wanted']:
    tk.Label(row5, image=icon_images['wanted'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
global wantedanswer
tk.Label(row5, text="特别想去的地方:", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
wantedanswer = CapsuleEntry(row5, width=220, placeholder='如鼓浪屿/无')
wantedanswer.pack(side='left', padx=(6, 0))

# --- 出行人数 ---
row6 = tk.Frame(form_frame, bg=BG_COLOR)
row6.pack(fill='x', pady=4)
if icon_images['people']:
    tk.Label(row6, image=icon_images['people'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
global peopleanswer
tk.Label(row6, text="出行人数：", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
peopleanswer = CapsuleEntry(row6, width=60, placeholder='如2')
peopleanswer.pack(side='left', padx=(6, 0))

# --- 其他留言 ---
row7 = tk.Frame(form_frame, bg=BG_COLOR)
row7.pack(fill='x', pady=4)
if icon_images['other']:
    tk.Label(row7, image=icon_images['other'], bg=BG_COLOR).pack(side='left', padx=(0, 4))
global exanswer
tk.Label(row7, text="还有其他想对小仓鼠说的话吗⌯'▾'⌯：", font=('Arial', 12), bg=BG_COLOR, fg='black').pack(side='left')
exanswer = CapsuleEntry(row7, width=360, placeholder='可选')
exanswer.pack(side='left', padx=(6, 0))

# --- 完成按钮 ---
row8 = tk.Frame(form_frame, bg=BG_COLOR)
row8.pack(fill='x', pady=(16, 0))
# 保留按钮引用，便于调试
submit_btn = CapsuleButton(row8, text="完成！", command=collect_and_next, width=200, height=54)
submit_btn.pack(side='left', padx=(10, 0))

root.mainloop()
