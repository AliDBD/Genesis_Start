#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/12/15 16:13
# @Author : Genesis Ai
# @File : DB_Connect.py

# import os
# import pymysql
#
# db_username = os.environ.get('DB_USERNAME')
# db_password = os.environ.get('DB_PASSWORD')
# print('密码', db_password, '用户名', db_username)
#
# #将原始数据提取的ID储存到指定的表内
# def save_id(ids):
#     try:
#         # 建立数据库链接
#         with pymysql.connect(
#                 host='172.18.3.106',
#                 user=f'{db_username}',
#                 password=f'{db_password}',
#                 database='test_ljy'
#         ) as conn:
#             # 创建一个Cursor对象来执行SQL
#             with conn.cursor() as cursor:
#                 for id in ids:
#                     sql = f'insert into xhs_search (search_id,type) values ("{id}",1)'
#                     # 执行SQL语句
#                     print(sql)
#                     cursor.execute(sql)
#                     # 提交
#                     print("ID写入完成！")
#                     conn.commit()
#     except pymysql.MySQLError as e:
#         print(f"Faild to connect to mysql:{e}")
#
# #将最终数据写入到指定表内
# def save_data(keywords, description, og_images,reid):
#     try:
#         # 建立数据库链接
#         with pymysql.connect(
#                 host='172.18.3.106',
#                 user=f'{db_username}',
#                 password=f'{db_password}',
#                 database='test_ljy'
#         ) as conn:
#             # 创建一个Cursor对象来执行SQL
#             with conn.cursor() as cursor:
#                 og_images_str = ','.join(og_images)
#                 #1=外贸；2=情感；3=穿搭;4=白领、职业形象;5=高尔夫球、美女
#                 sql = f'insert into xhs_json (label,Copywriting,image,type,shop_id) values ("{keywords}", "{description}", "{og_images_str}", 5,"{reid}")'
#                 # 执行SQL语句
#                 print(f"执行的sql语句：{sql}")
#                 cursor.execute(sql)
#                 # 提交
#                 conn.commit()
#                 print("数据写入数据库完成！")
#     except pymysql.MySQLError as e:
#         print("save_data方法写入错误！")
#         print(f"Faild to connect to mysql:{e}")
#
# #查询表数据获取ID
# def find_id():
#     try:
#         # 建立数据库链接
#         with pymysql.connect(
#                 host='172.18.3.106',
#                 user=f'{db_username}',
#                 password=f'{db_password}',
#                 database='test_ljy'
#         ) as conn:
#             # 创建一个Cursor对象来执行SQL
#             id_list = []
#             cursor = conn.cursor()
#             cursor.execute(f'SELECT search_id FROM `xhs_search`')
#             results = cursor.fetchall()
#             extracted_value = [item[0] for item in results]
#     except pymysql.MySQLError as e:
#         print(f"Faild to connect to mysql:{e}")
#     return extracted_value
#
# def clear_disdata():
#     try:
#         # 建立数据库链接
#         with pymysql.connect(
#                 host='172.18.3.106',
#                 user=f'{db_username}',
#                 password=f'{db_password}',
#                 database='test_ljy'
#         ) as conn:
#             # 创建一个Cursor对象来执行SQL
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM `xhs_json` WHERE Copywriting =''")
#             conn.commit()
#
#             cursor.close()
#             conn.close()
#             print("数据清理完成！")
#     except pymysql.MySQLError as e:
#         print(f"Faild to connect to mysql:{e}")
#
# #清空ID表
# def clear_sheet():
#     try:
#         # 建立数据库链接
#         with pymysql.connect(
#                 host='172.18.3.106',
#                 user=f'{db_username}',
#                 password=f'{db_password}',
#                 database='test_ljy'
#         ) as conn:
#             # 创建一个Cursor对象来执行SQL
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM xhs_search")
#             conn.commit()
#
#             cursor.close()
#             conn.close()
#             print("数据清理完成！")
#     except pymysql.MySQLError as e:
#         print(f"Faild to connect to mysql:{e}")


import pymysql
import os

def get_db_connection():
    return pymysql.connect(host='172.18.3.106',
                           user=os.getenv('DB_USERNAME'),
                           password=os.getenv('DB_PASSWORD'),
                           database='test_ljy')

def execute_query(query, params=None):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
    finally:
        conn.close()

def save_id(ids):
    for id in ids:
        execute_query('insert into xhs_search (search_id, type) values (%s, 1)', (id,))

def save_data(keywords, description, og_images, reid):
    og_images_str = ','.join(og_images)
    execute_query('insert into xhs_json (label, Copywriting, image, type, shop_id) values (%s, %s, %s, 5, %s)',
                  (keywords, description, og_images_str, reid))

def clear_table(table_name):
    execute_query(f'DELETE FROM `{table_name}`')
