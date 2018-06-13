#!/user/bin/python
#-*- coding:utf-8 -*-

from urllib import request
from urllib import parse
import json

def youdaoTranslate(value, count):
    if value == '':
        print('输入内容为空@_@请重新输入!')
        return False
    else:
        # Request URL
        responseURL = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        # 待提交准备Post给url的Data:定义为dict
        form_Data = {}
        form_Data['i'] = value
        form_Data['from'] = 'AUTO'
        form_Data['to'] = 'AUTO'
        form_Data['smartresult'] = 'dict'
        form_Data['client'] = 'fanyideskweb'
        form_Data['doctype'] = 'json'
        form_Data['version'] = '2.1'
        form_Data['keyfrom'] = 'fanyi.web'
        form_Data['action'] = 'FY_BY_REALTIME'
        form_Data['typoResult'] = 'false'
        # 使用urlencode方法转换标准格式　
        data = parse.urlencode(form_Data).encode('utf-8')
        response = request.urlopen(responseURL,data)
        html = response.read().decode('utf-8')
        # 使用JSON
        translate_result = json.loads(html)
        # print(translate_result)
        # 找到翻译结果
        # 这里推荐一个格式化JSON的好工具：https://c.runoob.com/front-end/53
        translate_result_main = translate_result['translateResult'][0][0]['tgt']
        # 打印翻译结果
        # print(f"待翻译的词句：{form_Data['i']}")
        # print(f'翻译的结果是：{translate_result_main}\n\n')
        print(f'{count}. {translate_result_main}\n\n')
        return True
    
if __name__ == '__main__':
    try:
        count = 1
        while True:
            print('-'*26)
            word = input('请输入待翻译的单词或句子:\n').strip()
            if youdaoTranslate(word, count) == True:
                count += 1
    except KeyboardInterrupt:
        print('手动退出!欢迎再来')
    
