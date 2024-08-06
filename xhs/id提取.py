#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/11 17:26

# @Author : linjingyu

# @File : id提取.py

import json
import pandas as pd

# JSON文件路径
json_path = r'E:\2023年\spider\notesdata.json'

# 读取JSON数据
with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 获取items列表
items = data['data']['items']

# 初始化列表，用于存储每行的数据
data_list = []

# 遍历items，提取xsec_token和id
for item in items:
    xsec_token = item.get('xsec_token', None)
    id_value = item.get('id', None)
    data_list.append({'xsec_token': xsec_token, 'id': id_value})

# 将数据转换为DataFrame
df = pd.DataFrame(data_list)

# Excel文件保存路径
excel_path = r'E:\2023年\spider\userID.xlsx'

# 保存到Excel，不包含索引
df.to_excel(excel_path, index=False)

print('数据已保存到Excel文件。')
