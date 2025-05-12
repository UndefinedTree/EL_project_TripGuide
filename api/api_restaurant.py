import os
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Application
biz_params = {
    # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换<YOUR_TOOL_ID>
    "user_defined_params": {
        "<YOUR_TOOL_ID>": {
            "article_index": 2}}}
def get_restaurant(prompt):
    global hotel_list
    response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key='sk-1434851a216f41feadb08b5afcbf2223',
    app_id='67b71af922144b058144b481bbd4a4b1',
    prompt=prompt,
    biz_params=biz_params)
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        return None
    else:
        # print('%s\n' % response.output.text)  # 在终端输出一次原始的，api返回的字符串
        # print('%s\n' % (response.usage))
        out_string = response.output.text
        restaurant_list = out_string.split('\n')
        return restaurant_list       #返回一个酒店名的列表

#测试部分
input = '南京'
restaurantList = get_restaurant(input)
for restaurant in restaurantList:
    print(restaurant)