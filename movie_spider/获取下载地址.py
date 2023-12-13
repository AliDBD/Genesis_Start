#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/12/12 17:12
# @Author : Genesis Ai
# @File : 获取下载地址.py
'''
代码仅提供逻辑，相似场景和应用基于此逻辑方法可以实现，具体内容和数据需求需要适当调整解析方式
本代码主要是根据需求获取某站点的可下载url链接（mp4格式）储存到本地
'''

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
excel_path = r'E:\2023年\spider\href.xlsx'
links = pd.read_excel(excel_path)['href']
#初始化一个列表保存地址
mp4_links = []
for link in links:
    time.sleep(1)
    url = f'https://www.111.com{link}'
    response = requests.get(url)
    if response.status_code == 200:
        html_data = response.text
        soup = BeautifulSoup(html_data,'html5lib')
        for tag in soup.find_all(True):
            if 'value' in tag.attrs:
                value = tag['value']
                if re.match(r'.*\.mp4$',value):
                    print(value)
                    mp4_links.append(value)
df = pd.DataFrame(mp4_links,columns=['href'])
#保存dataframe到excel文件中
output_excel_path = f'E:/2023年/spider/loading_url.xlsx'
df.to_excel(output_excel_path,index = False)
print(f"所有的下载地址已经保存到：{output_excel_path}")
