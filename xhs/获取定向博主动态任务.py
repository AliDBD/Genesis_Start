#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/1/29 14:28
# @Author : Genesis Ai
# @File : 获取定向博主动态任务.py

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import time
import random

def ghome_html():
    url = 'https://www.xiaohongshu.com/user/profile/'
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.xiaohongshu.com',
        'Connection': 'keep-alive'
    }
    time_code = random.randint(2,10)
    id = '55c7c08bf5a263301cf1c9b2'
    print(f"请求ID：{id}")
    time.sleep(time_code)
    username = 't17037773479161'
    password = 'lhlnpdmj'
    proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
    response = requests.get(url + id, headers=headers, proxies={'http': proxy, 'https': proxy})
    if response.status_code == 200:
        html_data = response.text
        print(html_data)
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

def new_id(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    note_id_pattern = r'"noteId":"(\w+)"'
    note_ids = re.findall(note_id_pattern, str(soup))
    print("Note IDs:", note_ids)  # 打印以检查note_ids

    timestamp_pattern = r'"publishTime":(\d+)'
    timestamps = re.findall(timestamp_pattern, str(soup))
    print("Timestamps:", timestamps)  # 打印以检查timestamps

    combined_list = list(zip(note_ids, timestamps))
    combined_list.sort(key=lambda x: x[1], reverse=True)

    most_recent_note_id = combined_list[0][0] if combined_list else None
    print("Most recent note ID:", most_recent_note_id)  # 打印最新的noteId

file_path = 'E:\\2023年\\spider\\error.txt'
new_id(file_path)

