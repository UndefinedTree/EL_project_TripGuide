# encoding:utf-8
import requests

# 接口地址
url = "https://api.map.baidu.com/geocoding/v3"

# 此处填写你在控制台-应用管理-创建应用后获取的AK
ak = "kpzq8pQc4MfWrG98dXiK19MeciSt5FL7"

def get_location(city_name):
    params = {
        "address":    city_name,
        "output":    "json",
        "ak":       ak,

    }

    response = requests.get(url=url, params=params)
    if response:
        response_data = response.json()
        if response_data['status'] == 0:
            # Step 2. 获取定位结果
            result = response_data['result']

            # Step 3. 提取经纬度
            longitude = result['location']['lng']  # 经度
            latitude = result['location']['lat']  # 纬度

            # print(f"经度：{longitude}")
            # print(f"纬度：{latitude}")
            return {'lng':longitude,'lat':latitude}
        else:
            print("请求失败，状态码：", response_data['status'])
            return None
    return None


# location = get_location("南京市鼓楼区")
# print(location)