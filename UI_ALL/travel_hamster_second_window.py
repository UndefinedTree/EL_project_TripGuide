import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from travel_hamster_utils import CapsuleButton, BG_COLOR, PRIMARY_COLOR, icon_images

def show_second_window(root):
    new_window = tk.Toplevel(root)
    new_window.title("小仓鼠玩命赶工中...")
    new_window.geometry("450x350+500+300")
    new_window.configure(bg=BG_COLOR)
    tk.Label(new_window, text="小仓鼠已成功收集信息，欢迎进入下一个界面！", bg=BG_COLOR).pack(pady=20)

    # 创建一个居中框架用于进度条和按钮
    center_frame = tk.Frame(new_window, bg=BG_COLOR)
    center_frame.pack(expand=True, fill=tk.BOTH)

    # 添加进度条，使用主题蓝色
    style = ttk.Style()
    style.theme_use('default')
    style.configure('Blue.Horizontal.TProgressbar', 
                    background=PRIMARY_COLOR,  # 进度条前景色
                    troughcolor=BG_COLOR,      # 进度条背景色
                    bordercolor=PRIMARY_COLOR, 
                    lightcolor=PRIMARY_COLOR, 
                    darkcolor=PRIMARY_COLOR)
    
    progress_bar = ttk.Progressbar(center_frame, 
                                   orient='horizontal', 
                                   length=300, 
                                   mode='indeterminate', 
                                   style='Blue.Horizontal.TProgressbar')
    progress_bar.pack(pady=10, expand=True)
    progress_bar.start(15)

    def next_window():
        new_window.destroy()
        import travel_hamster_third_window
        travel_hamster_third_window.show_third_window(root)

    CapsuleButton(center_frame, text="确认", command=next_window).pack(pady=30)