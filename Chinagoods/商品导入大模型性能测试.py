#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/7/5 10:31
# @Author : Genesis Ai
# @File : 商品导入大模型性能测试.py

import json
import re
import requests
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_items(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def login(username, password):
    url = "https://testapiserver.chinagoods.com/login/web/auth/password"
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        "grant_type": "password",
        "scope": "USER",
        "username": username,
        "password": password
    })
    try:
        response = requests.post(url, headers=headers, data=data)
        json_data = json.loads(response.text)
        print(json_data)
        token = re.search(r'"access_token":\s*"([^"]+)"', json.dumps(json_data)).group(1)
        return token
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None


def model(token, origin_id, cover_pic_list, goods_title):
    url = "https://testapiserver.chinagoods.com/detector/seller/save/model"
    headers = {
        'Authorization': f"Bearer {token}",
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'testapiserver.chinagoods.com',
        'Connection': 'keep-alive'
    }
    data = json.dumps({
        "originId": origin_id,
        "coverPicList": cover_pic_list,
        "goodsTitle": goods_title,
        "attribute": "",
        "dictName": "件",
        "salePriceType": 1,
        "multistageJson": "",
        "salePrice": 799,
        "descPicList": [],
        "minSaleNo": 1
    })
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None


def main():
    username = "13408400153"
    password = "DqOxlLu0qOPKQCGApzYVc4dC/SFiKFZnOtmqQjWeS8VxanZpntZ1x5fKMGp3+40UptV8bviWKqujgw1ODJmlh+6wD14AGMsO1UpZyty0rMQjDHVlwdvzgPwBYUjhT8SErt5e2MF7L5NR1niCeJExL5OHRdoOdJ8OvZEeEztW8hM="

    token = login(username, password)
    if not token:
        print("Login failed")
        return

    items = load_items(r'E:\2024年\1688\extracted_data.json')
    if not items:
        print("Failed to load items")
        return

    num_requests = 20  # 并发请求数
    test_duration = 300  # 测试持续时间（秒）
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        while time.time() - start_time < test_duration:
            for i in range(num_requests):
                origin_data = random.randint(1888, 99999)
                origin_id = f"8877919{origin_data}"
                item = items[i % len(items)]  # 循环使用 items
                cover_pic_list = [
                    item["imageUrl"].get("imgUrl"),
                    item["imageUrl"].get("imgUrlOf100x100"),
                    item["imageUrl"].get("imgUrlOf120x120"),
                    item["imageUrl"].get("imgUrlOf150x150"),
                    item["imageUrl"].get("imgUrlOf220x220"),
                    item["imageUrl"].get("imgUrlOf270x270"),
                    item["imageUrl"].get("imgUrlOf290x290")
                ]
                cover_pic_list = [url for url in cover_pic_list if url]  # 过滤掉值为空的URL
                goods_title = item["simpleSubject"]
                futures.append(executor.submit(model, token, origin_id, cover_pic_list, goods_title))

            # 获取并处理所有完成的请求
            for future in as_completed(futures):
                result = future.result()
                print(result)
                futures.remove(future)  # 移除已完成的 future


if __name__ == '__main__':
    main()
