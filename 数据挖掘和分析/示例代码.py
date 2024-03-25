#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/2/20 21:00
# @Author : Genesis Ai
# @File : 示例代码.py


import requests
from bs4 import BeautifulSoup
def fetch_and_parse_url(url):
    """
    抓取给定URL的网页内容，并使用BeautifulSoup解析HTML，提取特定数据。
    参数:
    - url: 要抓取的网页的URL字符串。
    返回:
    - 数据列表: 从网页中提取的数据项列表。
    """
    # 使用requests库发送HTTP请求，获取网页内容
    response = requests.get(url)
    # 确保请求成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 示例：提取所有的h1标签内容
        # 注意：根据需要提取的内容，这里的选择器可以修改
        data_items = soup.find_all('h1')
        # 提取文本数据
        extracted_data = [item.text for item in data_items]
        return extracted_data
    else:
        print("网页请求失败，状态码:", response.status_code)
        return []
# 示例URL
url = 'http://www.baidu.com'
data = fetch_and_parse_url(url)
print("提取的数据:", data)
