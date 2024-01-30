#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/1/29 14:28
# @Author : Genesis Ai
# @File : 获取定向博主动态任务.py

import pandas as pd
import requests
import re
def get_html():
    # 读取Excel文件并提取ID
    file_path_excel = 'E:\\2023年\\spider\\userID.xlsx'
    df = pd.read_excel(file_path_excel)
    ids = df['ID'].tolist()  # 确保列名与您的文件匹配

    # 基础URL
    base_url = 'https://www.xiaohongshu.com/user/profile/'

    # 用于存储响应HTML的文件路径
    output_file = 'E:\\2023年\\spider\\user_html.txt'

    # 对于每个ID，发起GET请求并保存响应
    with open(output_file, 'w', encoding='utf-8') as file:
        for user_id in ids:
            response = requests.get(base_url + user_id)
            if response.status_code == 200:
                file.write(response.text + '\n\n')  # 将响应内容写入文件
            else:
                file.write(f'Failed to fetch data for ID {user_id}\n\n')

    print("请求完成，响应已保存到文件。")
    #
    # @staticmethod
    # # 函数：从文件中读取并提取所有的noteId
    # def extract_noteIds(file_path):
    #     noteIds = []
    #     pattern = r'\"noteId\":\"([^\"]+)\"'
    #
    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             matches = re.findall(pattern, line)
    #             for match in matches:
    #                 noteIds.append(match)
    #     save_id(noteIds)
    #     return noteIds
    #
    # # 使用这个函数提取noteId
    # file_path = 'E:\\2023年\\spider\\user_html.txt'  # 替换为您的文件路径
    # noteIds = extract_noteIds(file_path)
    #
    # # 输出提取到的noteId
    # print(noteIds)

get_html()