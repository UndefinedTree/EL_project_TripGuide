import os
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Application
import re

biz_params = {
    # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换<YOUR_TOOL_ID>
    "user_defined_params": {
        "<YOUR_TOOL_ID>": {
            "article_index": 2}}}
def get_navigation(prompt):
    response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key='sk-1434851a216f41feadb08b5afcbf2223',
    app_id='001a689574c4479f8512948eb4db1c9a',
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

        return output


#测试部分
input = '南京大学鼓楼校区，南京鸡鸣寺'

output = get_navigation(input)

print(output)