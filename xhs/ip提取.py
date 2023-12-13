#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/13 10:38

# @Author : Genesis Ai

# @File : ip提取.py
import time

import pandas as pd
import requests


import requests

# def poxie():
    # 代理信息
    # proxy_ip = "d842.kdltps.com"
    # proxy_port = 15818
    # username = "t17037123479161"
    # password = "123456"
    # proxies = {
    #     "http": f"http://{username}:{password}@{proxy_ip}:{proxy_port}",
    #     "https": f"https://{username}:{password}@{proxy_ip}:{proxy_port}",
    # }
    #
    # # 目标 URL
    # url = "https://ip.cn/api/index?ip=&type=0"
    #
    # # 使用代理发出 GET 请求
    # try:
    #     response = requests.get(url, proxies=proxies)
    #     print(response.text)
    # except Exception as e:
    #     print(f"发生错误: {e}")

ip_data = []
for i in range(5):
    time.sleep(
        2
    )
    url = 'https://ip.cn/api/index?ip=&type=0'
    username = 't17037773479161'
    password = 'lhlnpdmj'
    proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
    try:
        result = requests.get(url, proxies={
            'http': proxy,
            'https': proxy
        })
        ip = result.json()['ip']
        address = result.json()['address']
        print(f"\nIP归属地：{address},IP地址：{ip}")
        ip_data.append({"归属地":address,"IP":ip})
    except (requests.RequestException,Exception) as e:
        print("请求失败！")

df = pd.DataFrame(ip_data)
df.to_excel(r'E:\2023年\spider\temp_ip.xlsx', index=False)
print("ip保存本地完成！")


