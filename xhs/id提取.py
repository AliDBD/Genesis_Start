#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/11 17:26

# @Author : linjingyu

# @File : id提取.py

import json
import pandas as pd
from xhs.DB_Connect import Connect

def extract_ids_to_excel(json_file_path, excel_file_path):
    # 加载 JSON 数据
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # 检查 'data' 和 'items' 键是否存在，并从中提取 IDs
    if 'data' in json_data and 'items' in json_data['data'] and isinstance(json_data['data']['items'], list):
        ids = [item['id'] for item in json_data['data']['items']]
    else:
        ids = []
    # 将 IDs 保存到 DataFrame 中
    df = pd.DataFrame(ids,columns=['ID'])
    # 将 DataFrame 保存到 Excel 文件中
    df.to_excel(excel_file_path, index=False)
    print(f"成功提取了 {len(ids)} 个 ID，并保存到了 '{excel_file_path}'。")
    Connect(ids)

# 使用示例
json_file_path = 'E:\\2023年\\spider\\json.txt'  # JSON 文件的路径
excel_file_path = 'E:\\2023年\\spider\\search_id.xlsx'  # Excel 文件的保存路径
#保存到本地路径
extract_ids_to_excel(json_file_path, excel_file_path)
