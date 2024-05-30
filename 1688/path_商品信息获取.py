#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/5/28 16:43
# @Author : Genesis Ai
# @File : path_商品信息获取.py
'''
此脚本仅用于本地固定格式json内容解析
基于本地数据，无需网络服务.
'''

import os
import json
import pandas as pd
from datetime import datetime

def extract_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        extracted_data = []
        for item in json_data:
            simple_subject = item.get('simpleSubject', 'N/A')
            detail_url = item.get('detailUrl', 'N/A')
            price = item.get('price', 'N/A')
            extracted_data.append({
                '商品标题': simple_subject,
                '商品链接': detail_url,
                '商品价格': price
            })
        return extracted_data

def save_data_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    directory = input("请输入包含 JSON 文件的目录路径: ")
    if not os.path.isdir(directory):
        print("无效的目录路径")
    else:
        all_extracted_data = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                extracted_data = extract_data_from_json(file_path)
                all_extracted_data.extend(extracted_data)

        if all_extracted_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(directory, f'清洗数据结果_{timestamp}.xlsx')
            save_data_to_excel(all_extracted_data, output_file)
            print(f"数据已保存到 {output_file}")
        else:
            print("没有提取到数据")
