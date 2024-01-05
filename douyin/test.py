#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/22 13:53
# @Author : Genesis Ai
# @File : test.py
import json
import pandas as pd
import matplotlib.pyplot as plt

def extract_ids_to_excel(file_path, excel_file_path):
    aweme_ids = []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if 'aweme_list' in data and isinstance(data['aweme_list'], list):
        aweme_ids = [item.get('aweme_id') for item in data['aweme_list']
                     if 'aweme_id' in item]
        keywords = [item.get('desc') for item in data ['aweme_list'] if 'desc' in item]

        df = pd.DataFrame(aweme_ids,keywords,columns=['ID','keywords'])
        df.to_excel(excel_file_path,index=False)
    print(aweme_ids)
    return aweme_ids

def main():
    file_path = 'E:\\2023年\\spider\\wb_json.txt'
    excel_file_path = 'E:\\2023年\\spider\\wb_search_id.xlsx'
    extract_ids_to_excel(file_path,excel_file_path)


if __name__ == '__main__':
    main()


# import json
#
# def extract_aweme_ids(file_path,excel_file_path):
#     aweme_ids = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             # 检查这一行是否包含 'aweme_id'
#             if '"aweme_id":' in line:
#                 # 尝试提取 'aweme_id' 字段
#                 try:
#                     # 为了处理可能的格式问题，我们从这一行构建一个小的JSON对象
#                     line_json = json.loads('{' + line.strip() + '}')
#                     aweme_id = line_json.get('aweme_id')
#                     if aweme_id:
#                         aweme_ids.append(aweme_id)
#                 except json.JSONDecodeError:
#                     continue  # 如果这一行无法解析为JSON，继续下一行
#     return aweme_ids
#
# # 使用此函数从文件中提取 aweme_id
# file_path = 'E:\\2023年\\spider\\wb_json.txt'  # 替换为您的文件路径
# excel_file_path = 'E:\\2023年\\spider\\wb_search_id.xlsx'
# aweme_ids = extract_aweme_ids(file_path,excel_file_path)
#
# # 显示提取结果
# print(aweme_ids[:10])  # 打印前10个aweme_id作为示例
