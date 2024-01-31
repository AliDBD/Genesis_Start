#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/1/30 9:19
# @Author : Genesis Ai
# @File : 获取ID储存到数据库.py
#定向博主ID，获取储存到本地数据库

import pandas as pd
from xhs.DB_Connect import store_values_in_database

def read_excel_and_get_ids(file_path):
    # 读取Excel文件
    print("开始读取excel文档数据。。。。。。")
    df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        id=row['ID']
        store_values_in_database(id)
    return id

file_path = 'E:\\2023年\\spider\\userID.xlsx'  # 替换为你的Excel文件路径
ids = read_excel_and_get_ids(file_path)