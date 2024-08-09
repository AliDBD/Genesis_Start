#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/8/6 17:08
# @Author : Genesis Ai
# @File : image_loading.py

import pymysql
import requests
from pathlib import Path
import os

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
print('密码', db_password, '用户名', db_username)


# 数据库配置
db_config = {
    'host':'172.18.3.106',
    'user':db_username,
    'password':db_password,
    'database':'test_ljy'
}

# 连接到MySQL数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 创建保存图片的文件夹
folder_path = Path('E:/图片/xhs_image')
folder_path.mkdir(parents=True, exist_ok=True)

# 从数据库读取图片链接
cursor.execute("SELECT image FROM `xhs_json`")
rows = cursor.fetchall()

# 下载图片
for row in rows:
    image_links = row[0].split(',')
    for link in image_links:
        try:
            response = requests.get(link.strip())
            if response.status_code == 200:
                # 提取图片名称或者使用UUID生成一个唯一的文件名
                image_name = link.split('/')[-1]
                file_path = folder_path / image_name
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"下载链接：{image_links}")
                print(f"Downloaded {image_name}")
            else:
                print(f"Failed to download {link}")
        except Exception as e:
            print(f"Error downloading {link}: {e}")

# 关闭数据库连接
cursor.close()
conn.close()
