#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/20 16:38
# @Author : Genesis Ai
# @File : wb_request.py

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import random

class Date_request:

    # 输入参数！
    @staticmethod
    def user_input():
        user_input = input("请输入关键字：")
        check = input(f"输入的值为:{user_input},确认输入y，重新输入输入n：")

        if check == "y":
            print(f"已确认输入的关键字为：{user_input}")
            return user_input  # 返回确认的关键字
        elif check == "n":
            print("请重新输入！")
            return None  # 如果需要，可以返回None或其他默认值
        else:
            print(f"输入的值无效：{check}")
            return None  # 如果需要，可以返回None或其他默认值

    def wb_search(self,keywords):
        url = f"https://s.weibo.com/weibo?q={keywords}"
        headers = {
           'Host': ' s.weibo.com',
           'Connection': ' keep-alive',
           'sec-ch-ua': ' "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
           'sec-ch-ua-mobile': ' ?0',
           'sec-ch-ua-platform': ' "Windows"',
           'Upgrade-Insecure-Requests': ' 1',
           'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
           'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'Sec-Fetch-Site': ' same-site',
           'Sec-Fetch-Mode': ' navigate',
           'Sec-Fetch-User': ' ?1',
           'Sec-Fetch-Dest': ' document',
           'Referer': ' https://weibo.com/',
           'Accept-Language': ' zh-CN,zh;q=0.9',
           'Cookie': ' SINAGLOBAL=6302283632516.203.1655965546784; SUB=_2AkMTJS-Mf8NxqwFRmPgdzWrgboh2zADEieKled5XJRMxHRl-yT9kqlAAtRB6OKUBY715K2tho8CVinmCcNlfNH7y-d0h'
        }
        time_code = random.randint(2,8)
        time.sleep(time_code)
        username = 't17037773479161'
        password = 'lhlnpdmj'
        proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
        response = requests.get(url=url, headers=headers, proxies={'http': proxy, 'https': proxy})
        html_date = response.text


# 调用函数
Date_request.user_input()

