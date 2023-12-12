#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/12 16:06

# @Author : Genesis Ai

# @File : 读取本地excel批量提取下载地址url.py
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

excel_path = r'E:\2023年\spider\index_url.xlsx'
url_list = pd.read_excel(excel_path)["url"]
#初始化一个列表来储存所有提取的href值
all_href_values = []
#遍历url列表
for url in url_list:
    time.sleep(2)
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        html_data = response.text
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html_data, 'html.parser')

        # 查找所有的<dt class="preview-item">并提取其中的href值
        for dt in soup.find_all('dt', class_='preview-item'):
            a_tag = dt.find('a', href=True)
            if a_tag:
                all_href_values.append(a_tag['href'])
    else:
        print(f"访问失败：{url}")
df = pd.DataFrame(all_href_values,columns=['href'])
#保存dataframe到excel文件中
output_excel_path = f'E:/2023年/spider/href.xlsx'
df.to_excel(output_excel_path,index = False)
print(f"所有的href值已经保存到：{output_excel_path}")