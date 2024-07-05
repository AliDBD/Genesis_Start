#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/7/5 9:05
# @Author : Genesis Ai
# @File : 商品导入大模型压测.py

#导入依赖包
import json
import re
import requests

#登录
def login():
    url  ="https://testapiserver.chinagoods.com/login/web/auth/password"
    headers = {
        # 'Host':'<calculated when request is sent>',
        'Content-Length': '<calculated when request is sent>',
        'Content-Type': 'application/json'
    }
    #请求体
    data = json.dumps({
        "grant_type": "password",
        "scope": "USER",
        "username": "13408400153",
        "password": "DqOxlLu0qOPKQCGApzYVc4dC/SFiKFZnOtmqQjWeS8VxanZpntZ1x5fKMGp3+40UptV8bviWKqujgw1ODJmlh+6wD14AGMsO1UpZyty0rMQjDHVlwdvzgPwBYUjhT8SErt5e2MF7L5NR1niCeJExL5OHRdoOdJ8OvZEeEztW8hM="
    })
    #执行请求并接收数据
    response = requests.post(url,headers=headers,data=data)
    json_data = json.loads(response.text)
    print(json_data)
    token=re.search(r'"access_token":\s*"([^"]+)"', json.dumps(json_data)).group(1)
    return token

def model(token):
    url = "https://testapiserver.chinagoods.com/detector/seller/save/model"
    headers = {
        'Authorization' : f"Bearer {token}",
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'testapiserver.chinagoods.com',
        'Connection': 'keep-alive'
    }

    data = json.dumps({
        "originId": 777791914781,
        "coverPicList": [
            "https://cbu01.alicdn.com/img/ibank/O1CN0158YynQ1XSmdnAokCJ_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01z66k851XSmeqfiXBS_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01E0ewrY1XSmeonZkWx_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01gWjhY31XSmdu9wc4W_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01ep6jbE1XSmdpGt4Ro_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01H3iZnE1XSmeQBTAl7_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN010X6WBa1XSmdq4Ip64_!!2217481422923-0-cib.jpg",
            "https://cbu01.alicdn.com/img/ibank/O1CN01mpzCAC1XSme4aJ6FD_!!2217481422923-0-cib.jpg"
        ],
        "goodsTitle": "小胸显大聚拢提拉平胸专用加厚8cm内衣女不空杯无钢圈馒头杯文胸",
        "attribute": "",
        "dictName": "件",
        "salePriceType": 1,
        "multistageJson": "",
        "salePrice": 799,
        "descPicList": [],
        "minSaleNo": 1
    })
    response = requests.post(url,headers=headers,data=data)
    print(headers)
    json_data = response.json()
    return json_data

def main():
    token = login()
    print(token)
    respnse_json = model(token)
    print(respnse_json)

if __name__ == '__main__':
    main()