import os
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Application
import re
from weather import Weather

biz_params = {
    # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换<YOUR_TOOL_ID>
    "user_defined_params": {
        "<YOUR_TOOL_ID>": {
            "article_index": 2}}}
def get_weather(prompt):
    response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key='sk-1434851a216f41feadb08b5afcbf2223',
    app_id='f5e7d3a706284624a5d781d846fe8539',
    prompt=prompt,
    biz_params=biz_params)
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        return None
    else:
        # print('%s\n' % response.output.text)  # 处理只输出文本text
        # print('%s\n' % (response.usage))

        output = response.output.text

        # 预处理：压缩连续换行符为单个，并去除首尾空白
        clean_text = ' '.join(output.split())  # 压缩所有空白字符为单个空格
        clean_text = clean_text.replace(' 白天', '\n白天').replace(' 夜晚', '\n夜晚').replace(' 温度', '\n温度')

        # 定义正则表达式模式
        date_pattern = re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日')
        day_weather_pattern = re.compile(r'白天天气：(.+)')
        night_weather_pattern = re.compile(r'夜晚天气：(.+)')
        temp_pattern = re.compile(r'温度：(\d+)°C / (\d+)°C')

        # 初始化结果列表
        weather_data = []

        # 将文本按日期分割
        date_blocks = re.split(r'(\d{4}年\d{1,2}月\d{1,2}日)', clean_text)[1:]  # 跳过第一个空元素

        for i in range(0, len(date_blocks), 2):
            date_str = date_blocks[i]
            block = date_blocks[i + 1]

            # 提取日期
            date_match = date_pattern.search(date_str)
            if date_match:
                year, month, day = map(int, date_match.groups())

                # 提取天气和温度
                day_weather = day_weather_pattern.search(block).group(1).strip()
                night_weather = night_weather_pattern.search(block).group(1).strip()
                temp_match = temp_pattern.search(block)
                high_temp = int(temp_match.group(1))
                low_temp = int(temp_match.group(2))




        return


#测试部分
input = '南京，2025年5月10日，3天'

output = get_weather(input)

print(output)