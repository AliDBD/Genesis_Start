#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/12/15 16:13
# @Author : Genesis Ai
# @File : DB_Connect.py

import os
import pymysql

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
print('密码', db_password, '用户名', db_username)

#定向ID储存
def save_id(ids):
    try:
        with pymysql.connect(
                host='172.18.3.106',
                user=f'{db_username}',
                password=f'{db_password}',
                database='test_ljy'
        ) as conn:
            with conn.cursor() as cursor:
                for id, user_id in ids:  # 解包元组
                    sql = '''
                        INSERT INTO xhs_search (search_id, user_id, type)
                        SELECT %s, %s, 1
                        WHERE NOT EXISTS (
                            SELECT 1 FROM xhs_search WHERE search_id = %s AND user_id = %s
                        )
                    '''
                    cursor.execute(sql, (id, user_id, id
                                         , user_id))  # 使用四个参数
                    conn.commit()
                    print("ID写入完成！")
    except pymysql.MySQLError as e:
        print(f"save_idFaild to connect to mysql:{e}")

#将原始数据提取的ID储存到指定的表内
def apach_save_id(ids):
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
                    sql = f'insert into xhs_search (search_id,type) values ("{id}",1)'
                    # 执行SQL语句
                    print(sql)
                    cursor.execute(sql)
                    # 提交
                    print("ID写入完成！")
                    conn.commit()
    except pymysql.MySQLError as e:
        print(f"save_idFaild to connect to mysql:{e}")

#将最终数据写入到指定表内
def save_data(keywords, description, og_images,reid):
    serce = 'ON'
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
                og_images_str = ','.join(og_images)
                #1=外贸；2=情感；3=穿搭;4=白领、职业形象;5=高尔夫球、美女
                sql = f'insert into xhs_json (label,Copywriting,image,type,shop_id,create_time,update_time,used) values ("{keywords}", "{description}", "{og_images_str}", 5,"{reid}",CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,"{serce}")'
                # 执行SQL语句
                print(f"执行的sql语句：{sql}")
                cursor.execute(sql)
                # 提交
                conn.commit()
                print("数据写入数据库完成！")
    except pymysql.MySQLError as e:
        print("save_data方法写入错误！")
        print(f"save_data.Faild to connect to mysql:{e}")

#查询表数据获取ID
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
            id_list = []
            cursor = conn.cursor()
            cursor.execute(f'SELECT search_id FROM `xhs_search`')
            results = cursor.fetchall()
            extracted_value = [item[0] for item in results]
    except pymysql.MySQLError as e:
        print(f"find_id.Faild to connect to mysql:{e}")
    return extracted_value

def clear_disdata():
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
            cursor.execute("DELETE FROM `xhs_json` WHERE Copywriting =''")
            conn.commit()

            cursor.close()
            conn.close()
            print("json表为空数据清理完成！")
    except pymysql.MySQLError as e:
        print(f"clear_disdataFaild to connect to mysql:{e}")

#清空ID表
def clear_sheet():
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
            cursor.execute("DELETE FROM xhs_search")
            conn.commit()

            cursor.close()
            conn.close()
            print("数据清理完成！")
    except pymysql.MySQLError as e:
        print(f"clear_sheet.Faild to connect to mysql:{e}")

#xhs_json表单根据shopID进行数据去重
def dedupe_table():
    try:
        #建立数据库链接
        with pymysql.connect(host='172.18.3.106',
                user=f'{db_username}',
                password=f'{db_password}',
                database='test_ljy'
        ) as conn:
            #创建一个Cursor对象执行SQL
            cursor = conn.cursor()
            retdata = cursor.execute("SELECT DISTINCT shop_id FROM xhs_json")
            conn.commit()

            cursor.close()
            conn.close()
            print(f"清除xhs_json列表完成，返回数据：{retdata}")
    except pymysql.MySQLError as e:
        print(f"dedupe_table.Faild to connect to mysql:{e}")


#遍历获取需要的参数信息，储存到指定的库
# def store_values_in_database(xsec_token,search_id):
#     try:
#         with pymysql.connect(host='172.18.3.106',
#                 user=f'{db_username}',
#                 password=f'{db_password}',
#                 database='test_ljy'
#         ) as conn:
#             #sql = f'INSERT INTO `user` (user_id) VALUES ("{path}")'
#             sql = f'INSERT INTO xhs_search (search_id, xsec_token) VALUES ({xsec_token}, {search_id})'
#             print(sql)
#             curses = conn.cursor()
#             curses.execute(sql)
#             conn.commit()
#     except pymysql.MySQLError as e:
#         print(f"store_values_in_database.Faild to connect to mysql:{e}")

    # 遍历列表并将值插入到数据库中

def store_values_in_database(xsec_token, search_id):
    try:
        # 建立数据库连接
        conn = pymysql.connect(host='172.18.3.106',
                               user=db_username,
                               password=db_password,
                               database='test_ljy',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as cursor:
                # 使用参数化查询来避免SQL注入
                sql = 'INSERT INTO xhs_search (search_id, xsec_token) VALUES (%s, %s)'
                cursor.execute(sql, (search_id, xsec_token))
                conn.commit()  # 提交事务
        finally:
            conn.close()  # 确保即使发生错误也能关闭连接
    except pymysql.MySQLError as e:
        print(f"store_values_in_database.Failed to connect to MySQL: {e}")


def find_userid():
    try:
        # 建立数据库链接
        with pymysql.connect(
                host='172.18.3.106',
                user=f'{db_username}',
                password=f'{db_password}',
                database='test_ljy',
                cursorclass=pymysql.cursors.DictCursor
        ) as conn:
            # 创建一个Cursor对象来执行SQL
            cursor = conn.cursor()
            cursor.execute("SELECT search_id, xsec_token FROM xhs_search")
            results = cursor.fetchall()  # 获取所有记录
    except pymysql.MySQLError as e:
        print(f"find_userid.Faild to connect to mysql:{e}")
    return results

#user_id同步到xhs_json表单
def synchronous_userid():
    try:
        # 建立数据库连接
        conn = pymysql.connect(
            host='172.18.3.106',
            user=f'{db_username}',
            password=f'{db_password}',
            database='test_ljy'
        )

        # 使用 `with` 语句管理连接对象的上下文
        with conn:
            # 创建一个游标对象执行 SQL
            with conn.cursor() as cursor:
                sql = '''
                UPDATE xhs_json
                SET xhs_json.user_id = (
                    SELECT xhs_search.user_id
                    FROM xhs_search
                    WHERE xhs_search.search_id = xhs_json.shop_id
                )
                WHERE EXISTS (
                    SELECT 1
                    FROM xhs_search
                    WHERE xhs_search.search_id = xhs_json.shop_id
                )
                '''

                # 执行 SQL 语句
                cursor.execute(sql)

                # 提交事务
                conn.commit()

                # 输出成功信息
                print("user_id同步成功！")

    except pymysql.MySQLError as e:
        # 捕获并输出 MySQL 错误
        print(f"synchronous_userid. Failed to connect to MySQL: {e}")


# import pymysql
# import os
#
# def get_db_connection():
#     return pymysql.connect(host='172.18.3.106',
#                            user=os.getenv('DB_USERNAME'),
#                            password=os.getenv('DB_PASSWORD'),
#                            database='test_ljy')
#
# def execute_query(query, params=None):
#     try:
#         conn = get_db_connection()
#         with conn.cursor() as cursor:
#             cursor.execute(query, params)
#             conn.commit()
#     except pymysql.MySQLError as e:
#         print(f"数据库错误: {e}")
#     finally:
#         conn.close()
#
# def save_id(ids):
#     for id in ids:
#         execute_query('insert into xhs_search (search_id, type) values (%s, 1)', (id,))
#
# def save_data(keywords, description, og_images, reid):
#     og_images_str = ','.join(og_images)
#     execute_query('insert into xhs_json (label, Copywriting, image, type, shop_id) values (%s, %s, %s, 5, %s)',
#                   (keywords, description, og_images_str, reid))
#
# def clear_table(table_name):
#     execute_query(f'DELETE FROM `{table_name}`')