#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/5/28 16:43
# @Author : Genesis Ai
# @File : 关键词商品信息获取.py
'''
联网需求，设置代理目标
不建议使用
'''

import os
import json
import requests
import pandas as pd
from datetime import datetime

def get_price_display(html_content):
    # 简单地从网页源代码中提取 "priceDisplay" 值
    # 这里假设 "priceDisplay" 出现的位置固定且唯一
    start_marker = '"priceDisplay":"'
    start_index = html_content.find(start_marker)
    if start_index != -1:
        start_index += len(start_marker)
        end_index = html_content.find('"', start_index)
        if end_index != -1:
            return html_content[start_index:end_index]
    return None

def extract_data_from_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                for item in json_data:
                    simple_subject = item.get('simpleSubject')
                    detail_url = item.get('detailUrl')
                    if simple_subject and detail_url:
                        # 请求 detailUrl 获取网页源代码
                        username = 't17037773479161'
                        password = 'lhlnpdmj'
                        proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
                        response = requests.get(detail_url, proxies={'http': proxy, 'https': proxy})
                        if response.status_code == 200:
                            html_content = response.text
                            price_display = get_price_display(html_content)
                            data.append({
                                '名称': simple_subject,
                                'url链接': detail_url,
                                '价格（一般为阶梯价）': price_display
                            })
    return data

def save_data_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    import sys
    directory = input("请输入包含 JSON 文件的目录路径: ")
    if not os.path.isdir(directory):
        print("无效的目录路径")
        sys.exit(1)

    extracted_data = extract_data_from_json_files(directory)
    if extracted_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(directory, f'extracted_data_{timestamp}.xlsx')
        save_data_to_excel(extracted_data, output_file)
        print(f"数据已保存到 {output_file}")
    else:
        print("没有提取到数据")
