#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/8 14:06

# @Author : linjingyu

# @File : htmlui.py

import re
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import json
import http.client

class dros:
    @staticmethod
    def url_check():
        # 打开并读取原始文件
        file_path = 'E:\\2023年\\spider\\error.txt'
        with open(file_path, 'r') as file:
            content = file.readlines()

        # 将每个URL格式化，每个URL一行，并写入新文件
        formatted_file_path = 'E:\\2023年\\spider\\url_check.txt'  # 指定格式化后的文件路径

        with open(formatted_file_path, 'w') as formatted_file:
            for line in content:
                # 分离URLs
                urls = line.split(',')
                for url in urls:
                    # 写入每个URL到新的一行
                    formatted_file.write(url.strip() + '\n')

                    print(url)

    @staticmethod
    def url_list(urllist):
        formatted_list = []
        urls = urllist.split(',')
        for url in urls:
            formatted_url = url.strip()
            # print(formatted_url)

            conn = http.client.HTTPSConnection("uatapiserver.chinagoods.com")
            payload = json.dumps({
                "urlList": [formatted_url]
            })
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': 'uatapiserver.chinagoods.com',
                'Connection': 'keep-alive',
            }
            conn.request("POST", "/pms/v1/thirds/goods_pic/describe/change?pwd=makePicHappyLove", payload, headers)
            res = conn.getresponse()
            data = res.read()
            source_url = data.decode('utf-8')
            parsed_json = json.loads(source_url)
            data_values = parsed_json.get('data', [])
            url = data_values[0] if data_values else None

            if url:
                formatted_list.append(url)
        print(formatted_list)

        return formatted_list

    @staticmethod
    def test_Login_User():
            url = 'https://testkunapi.chinagoods.com/buyerapi/v1/auth/login'
            headers = {
                'Accept-Language': 'es',
                'Content-Type': 'application/json'
            }
            data = json.dumps({
                "username": "15361508912",
                "password": "abc123456",
                "grant_type": "password",
                "scope": "buyer",
                "area_code": "+86"
            })
            response = requests.post(url=url,headers=headers, data=data)
            if response.get('success'):
                tokens = response['data']["access_token"]  # 提取 access_token
                print("登录成功，token为：", tokens)
                return tokens
            else:
                print(f'登录账号：{data},登录url：{url}')
                print("登录失败！", response.get('error'))
# 新文件现在包含格式化后的URLs

def main():
    getoken = dros()
    urllist = 'http://sns-webpic-qc.xhscdn.com/202401311135/994686a0f89b58905a5e7c98905174d5/1040g2sg30ui68nlj541g4125tc08nidi142gk30!nd_dft_wlteh_jpg_3,http://sns-webpic-qc.xhscdn.com/202401311135/370c4784907fb588828e2d97e8432d10/1040g2sg30ui68nlj54104125tc08nidih4nk9v0!nd_dft_wlteh_jpg_3,http://sns-webpic-qc.xhscdn.com/202401311135/8def865f1c46f833f3a40964d146e469/1040g2sg30ui68nlj540g4125tc08nidi9t8q43o!nd_dft_wlteh_jpg_3,http://sns-webpic-qc.xhscdn.com/202401311135/ff37484ecb2f785850897c1d1056a833/1040g2sg30ui68nlj54004125tc08nidiek78nng!nd_dft_wlteh_jpg_3,http://sns-webpic-qc.xhscdn.com/202401311135/d10baf4bf799eeaf96d4bb8c0d06780c/1040g2sg30ui68nlj54204125tc08nidi5qepnu0!nd_dft_wlteh_jpg_3,http://sns-webpic-qc.xhscdn.com/202401311135/f18e4ca141e59e5298541bc665089b88/1040g2sg30ui68nlj54304125tc08nidicgnote0!nd_dft_wlteh_jpg_3,http://sns-webpic-qc.xhscdn.com/202401311135/376c4f9ada8fb5d75103be2fd9dffc47/1040g2sg30ui68nlj543g4125tc08nidig04fu3o!nd_dft_wlteh_jpg_3'
    getoken.url_list(urllist)

if __name__ == '__main__':
    main()