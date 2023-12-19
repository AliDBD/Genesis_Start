#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/19 11:33
# @Author : Genesis Ai
# @File : DB_test.py

import os
import pymysql

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
print('密码', db_password, '用户名', db_username)

def find_id():
    try:
        # 建立数据库链接
        with pymysql.connect(
                host='172.18.3.106',
                user=f'{db_username}',
                password=f'{db_password}',
                database='test_ljy'
        ) as conn:
            # 创建一个Cursor对象来执行SQL
            cursor = conn.cursor()
            cursor.execute(f'SELECT search_id FROM `xhs_search`')
            results = cursor.fetchall()
            extracted_value = [item[0] for item in results]
    except pymysql.MySQLError as e:
        print(f"Faild to connect to mysql:{e}")
    return extracted_value

ids=find_id()
print(ids)