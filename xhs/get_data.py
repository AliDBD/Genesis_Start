#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/7 13:42

# @Author : linjingyu

# @File : get_data.py
import random
import time

import pandas as pd
from bs4 import BeautifulSoup
import requests

def proxy():
    url = 'https://ip.cn/api/index?ip=&type=0'
    username = 't17037773479161'
    password = 'lhlnpdmj'
    proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
    result = requests.get(url, proxies={
        'http': proxy,
        'https': proxy
    })

    ip = result.json()['ip']
    print(ip)
    return ip


# 定义一个函数来解析HTML并提取所需字段
def parse_html(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')

    # 提取keywords和description
    keywords = soup.find('meta', attrs={'name': 'keywords'})
    if keywords is not None:
        keywords = keywords['content']
    else:
        keywords = ""
    description = soup.find('meta', attrs={'name': 'description'})
    if description is not None:
        description = description['content']
    else:
        description = ""

    # 提取og:image
    og_images = soup.find_all('meta', attrs={'name': 'og:image'})
    og_image_values = [img['content'] for img in og_images]

    return keywords, description, og_image_values

# 修改found_data()函数来返回所有请求的结果
def found_data():
    # 读取 Excel 文件中的数据，获取 ID
    excel_path = r'E:\2023年\spider\search_id.xlsx'
    seach_id = pd.read_excel(excel_path)['ID']
    time_code = random.randint(2,5)
    # 定义请求的 URL 和 headers
    url = "https://www.xiaohongshu.com/explore/"
    headers = {
        'User-Agent': 'AMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Host': 'www.xiaohongshu.com',
        'Connection': 'keep-alive'
    }
    # 创建一个空列表来存储请求结果
    results = []
    # 遍历 Excel 文件中的 ID，发送请求并处理响应
    for index, keywords in enumerate(seach_id):
        print(f"请求ID：{keywords} ({index})")
        time.sleep(time_code)
        username = 't17037773479161'
        password = 'lhlnpdmj'
        proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
        response = requests.get(url + keywords, headers=headers, proxies={'http': proxy,'https': proxy})
        if response.status_code == 200:
            html_data = response.text
            keywords, description, og_images = parse_html(html_data)
            print(response.text)
            # 将提取的数据添加到结果列表中
            results.append({'标签': keywords, '文案内容': description,
                            **{f'og:image{i + 1}': img for i, img in enumerate(og_images)}})
            print(f"响应内容：\n{html_data}\n")
        else:
            print(f"请求 {keywords} 失败，状态码： {response.status_code}")
    # 将结果列表返回
    return results

data_list = found_data()
# 将数据列表转换为DataFrame
df = pd.DataFrame(data_list)
# 将数据保存到本地Excel文件
df.to_excel(r'E:\2023年\spider\temp_data.xlsx', index=False)
