import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from travel_hamster_utils import CapsuleButton, BG_COLOR, PRIMARY_COLOR, icon_images
import api_hotel  # 导入api_hotel模块
import api_hotel_link  # 导入api_hotel_link模块
import api_restaurant  # 导入api_restaurant模块
import api_restaurant_link  # 导入api_restaurant_link模块
import api_train  # 导入api_train模块
import api_navigation  # 导入api_navigation模块
import api_air  # 导入api_air模块
import api_spot  # 导入api_spot模块

def show_second_window(root, startplace, destination, startyear, startmonth, startdate, days):
    # 调用api_hotel获取酒店信息
    hotel_list = api_hotel.get_hotel(destination)
    hotel_link_list = ["","",""]
    hotel_link_list[0] = api_hotel_link.get_hotel_link(f"{destination},{hotel_list[0]}")
    print("第一个酒店",hotel_list[0],hotel_link_list[0])
    hotel_link_list[1] = api_hotel_link.get_hotel_link(f"{destination},{hotel_list[1]}")
    print("第二个酒店",hotel_list[1],hotel_link_list[1])
    hotel_link_list[2] = api_hotel_link.get_hotel_link(f"{destination},{hotel_list[2]}")
    print("第三个酒店",hotel_list[2],hotel_link_list[2])

    # 调用api_restaurant获取餐厅信息
    restaurant_list = api_restaurant.get_restaurant(destination)
    restaurant_link_list = ["","",""]
    restaurant_link_list[0] = api_restaurant_link.get_restaurant_link(f"{destination},{restaurant_list[0]}")
    print("第一个餐厅",restaurant_list[0],restaurant_link_list[0])
    restaurant_link_list[1] = api_restaurant_link.get_restaurant_link(f"{destination},{restaurant_list[1]}")
    print("第二个餐厅",restaurant_list[1],restaurant_link_list[1])
    restaurant_link_list[2] = api_restaurant_link.get_restaurant_link(f"{destination},{restaurant_list[2]}")
    print("第三个餐厅",restaurant_list[2],restaurant_link_list[2])

    # 调用api_train获取火车信息
    train_link = api_train.get_train(f"{startplace}, {destination}, {startyear}年{startmonth}月{startdate}日")
    print("火车连接",train_link)

    # 调用api_air获取航班信息
    air_link = api_air.get_air(f"{startplace}, {destination}, {startyear}年{startmonth}月{startdate}日")
    print("航班连接",air_link)

    # 调用api_navigation获取导航信息
    nav_info = api_navigation.get_navigation(f"{startplace}, {destination}")
    print("导航信息：", nav_info)

    # 调用api_weather获取天气信息
    # weather_info = api_weather.set_weather_info(destination, startyear, startmonth, startdate)
    # if weather_info:
    #     print("天气信息：", weather_info)

    # 调用api_spot获取景点信息
    spot_list = ["" for _ in range(int(days))]
    spot_list = api_spot.get_spot(f"{destination},{days}")
    print("景点名称",spot_list)

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
        travel_hamster_third_window.show_third_window(root, startplace, destination, startyear, startmonth, startdate, days, hotel_list, hotel_link_list, restaurant_list, restaurant_link_list, train_link, air_link, nav_info,spot_list)

    CapsuleButton(center_frame, text="确认", command=next_window).pack(pady=30)