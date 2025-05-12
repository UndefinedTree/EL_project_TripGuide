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
def get_train(prompt):
    response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key='sk-1434851a216f41feadb08b5afcbf2223',
    app_id='66d9fe3c60604177a2a3a1db27196f84',
    prompt=prompt,
    biz_params=biz_params)
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        # print('%s\n' % response.output.text)  # 处理只输出文本text
        # print('%s\n' % (response.usage))

        # 由于ai的返回会有多余的文字，提取出单独的链接
        output = response.output.text
        url_pattern = re.compile(
            r'https?://\S+'
            r'(?=[\s]|$)',  # 仅允许空格或行尾
            re.IGNORECASE
        )
        match = url_pattern.search(output)
        if match:
            return match.group()
    return None


input = '南京，北京，2025年5月20日'

output = get_train(input)

print(output)