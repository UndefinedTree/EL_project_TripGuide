import tkinter as tk
from tkinter import messagebox
import requests


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

    tk.Button(new_window, text="确认", command=next_window).pack()


def collect_and_next():
    if validate_input():
        save_info()
        show_next_window()


root = tk.Tk()
root.title("travel hamster")
root.geometry("1000x650+250+100")

tk.Label(root, text="Welcome to travel hamster~!", font=('Arial', 16), width=1000, height=3,
         bg='lightblue').pack()
tk.Label(root, text="").pack()
tk.Label(root,
         text="💙欢迎光临旅行仓鼠的小屋~这里你可以通过告诉小仓鼠你的需求从而获得小仓鼠为你私人化定制的旅行计划₍ᐢ..ᐢ₎♡",
         font=('Arial', 12, 'bold')).pack()

tk.Label(root, text="出发地：", font=('Arial', 12)).place(x=280, y=170)
startanswer = tk.Entry(root, width=40, font=('Arial', 12))
startanswer.place(x=360, y=170)

tk.Label(root, text="目的地：", font=('Arial', 12)).place(x=280, y=210)
destinationanswer = tk.Entry(root, width=40, font=('Arial', 12))
destinationanswer.place(x=360, y=210)

tk.Label(root, text="出发日期：", font=('Arial', 12)).place(x=280, y=250)
dateyearanswer = tk.Entry(root, width=8, font=('Arial', 12))
dateyearanswer.place(x=370, y=250)
tk.Label(root, text='年', font=('Arial', 12)).place(x=440, y=250)
datemonthanswer = tk.Entry(root, width=3, font=('Arial', 12))
datemonthanswer.place(x=460, y=250)
tk.Label(root, text="月", font=('Arial', 12)).place(x=490, y=250)
dateanswer = tk.Entry(root, width=3, font=('Arial', 12))
dateanswer.place(x=510, y=250)
tk.Label(root, text="日", font=('Arial', 12)).place(x=540, y=250)

tk.Label(root, text="旅行天数：", font=('Arial', 12)).place(x=280, y=290)
sumdayanswer = tk.Entry(root, width=4, font=('Arial', 12))
sumdayanswer.place(x=370, y=290)
tk.Label(root, text="天", font=('Arial', 12)).place(x=390, y=290)

tk.Label(root, text="旅行目的：", font=('Arial', 12)).place(x=280, y=330)
tk.Label(root, text="特别想去的地方:", font=('Arial', 12)).place(x=280, y=370)
wantedanswer = tk.Entry(root, width=35, font=('Arial', 12))
wantedanswer.place(x=410, y=370)

tk.Label(root, text="出行人数：", font=('Arial', 12)).place(x=280, y=410)
peopleanswer = tk.Entry(root, width=3, font=('Arial', 12))
peopleanswer.place(x=370, y=410)

tk.Label(root, text="还有其他想对小仓鼠说的话吗⌯'▾'⌯：", font=('Arial', 12)).place(x=280, y=450)
exanswer = tk.Entry(root, width=60, font=('Arial', 12))
exanswer.place(x=280, y=490)

options = [
    "风景",
    "美食",
    "玩乐",
    "旅拍"
]
option_vars = []
x_position = 366
for option in options:
    var = tk.IntVar()
    option_vars.append(var)
    tk.Checkbutton(root, text=option, variable=var, font=('Arial', 12)).place(x=x_position, y=330)
    x_position += tk.Checkbutton(root, text=option, variable=var, font=('Arial', 12)).winfo_reqwidth() + 10

tk.Button(root, text="完成！", command=collect_and_next, font=('Arial', 13, 'bold'), bg='lightblue').place(x=460, y=540)

root.mainloop()
