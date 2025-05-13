import requests
from datetime import datetime
from api_location import get_location

# 加载环境变量（需创建 .env 文件）
API_KEY = '14338174ca4144ceb2a122758251305'  # 或直接赋值：API_KEY = 'your_key_here'


def get_weather(city_name):
    """
    获取未来14天天气预报（WeatherAPI免费版）
    参数：
    city_name - 支持中英文城市名（如"北京"、"Tokyo"）
    """
    location = get_location(city_name)
    q = f"{round(location["lat"],4)},{round(location["lng"],4)}"
    try:
        # 直接请求天气预报（无需坐标转换）
        url = "http://api.weatherapi.com/v1/forecast.json"
        params = {
            'key': API_KEY,
            'q': q,
            'days': 14,
            'lang': 'zh'  # 获取中文描述
        }

        response = requests.get(url, params=params)
        data = response.json()

        # 错误处理
        if 'error' in data:
            print(f"错误：{data['error']['message']}")
            return None

        # 解析数据
        weather_list = {}
        # print(f"\n{city_name} 未来14天天气预报：")
        for day in data['forecast']['forecastday']:
            date = datetime.strptime(day['date'], '%Y-%m-%d')
            weekday = date.strftime('%A')  # 自动适配系统语言（中文需系统支持）

            # 天气信息
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            condition = day['day']['condition']['text']
            rain_chance = day['day']['daily_chance_of_rain']

            # 中文星期处理（备选方案）
            chinese_weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            weekday_cn = chinese_weekdays[date.weekday()]

            # print(
            #     f"{date.month}/{date.day} {weekday_cn} | "
            #     f"温度：{min_temp}~{max_temp}℃ | "
            #     f"天气：{condition} | "
            #     f"降雨概率：{rain_chance}%"
            # )
            weather_list[f"{date.month}/{date.day}"] = \
                f"{date.month}/{date.day} {weekday_cn} | "\
                f"温度：{min_temp}~{max_temp}℃ | "\
                f"天气：{condition} | "\
                f"降雨概率：{rain_chance}%"
        return weather_list
    except Exception as e:
        print(f"发生错误：{str(e)}")
        return None


# 使用示例
weather = get_weather("南京市南京大学鼓楼校区")
print(weather)