#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/12/15 16:13
# @Author : Genesis Ai
# @File : DB_Connect.py

import os
import pymysql
# db_username = os.environ.get('DB_USERNAME')
# db_password = os.environ.get('DB_PASSWORD')
# print('密码',db_password,'用户名',db_username)
# try:
#     def Connect(ids):
#         #建立数据库链接
#         conn = pymysql.connect(
#             host = '172.18.3.106',
#             user = f'{db_username}',
#             password = f'{db_password}',
#             database = 'ghost_test'
#         )
#         #创建一个Cursor对象来执行SQL
#         cursor = conn.cursor()
#         for id in ids:
#             sql = f'insert into xhs_search (`search_id`) values (\'{id}\')'
#             #执行SQL语句
#             cursor.execute(sql)
#             #提交
#             conn.commit()
#         #关闭Cursor和Connection
#         cursor.close()
#         conn.close()
# except pymysql.MySQLError as e:
#     print(f"Faild to connect to mysql:{e}")

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
print('密码', db_password, '用户名', db_username)
def Connect(ids):
    try:
        # 建立数据库链接
        with pymysql.connect(
                host='172.18.3.106',
                user=f'{db_username}',
                password=f'{db_password}',
                database='test_ljy'
        ) as conn:
            # 创建一个Cursor对象来执行SQL
            with conn.cursor() as cursor:
                for id in ids:
                    sql = f'insert into xhs_search (search_id) values ("{id}")'
                    # 执行SQL语句
                    print(sql)
                    cursor.execute(sql)
                    # 提交
                    conn.commit()
    except pymysql.MySQLError as e:
        print(f"Faild to connect to mysql:{e}")