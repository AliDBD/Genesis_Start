#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2025/1/3 11:18
# @Author : Genesis Ai
# @File : tiktok_search_keywords.py
import requests

# 请求头和URL
url = "https://ads.tiktok.com/creative_radar_api/v1/script/keyword/list?page=1&limit=20&period=7&country_code=US&order_by=post&order_type=desc"
headers = {
    "Host": "ads.tiktok.com",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": "\"Windows\"",
    "timestamp": "1735873979",
    "lang": "zh",
    "user-sign": "445f42e170cfe7f9",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "anonymous-user-id": "3bd2b243-7f55-4a8c-bd17-29f22e4e356f",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "web-id": "7455517281448216080",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://ads.tiktok.com/business/creativecenter/keyword-insights/pad/zh",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "_ttp=2lzxLnayWdDdUZznjD1Sga9ljyM; tt_chain_token=ulA1PBY1TYLsTvC34E7WGw==; tiktok_webapp_lang=zh-Hans; lang_type=zh; _ga=GA1.1.363396326.1735873003; _ga_QQM0HPKD40=GS1.1.1735873002.1.1.1735873949.0.0.1233974711; i18next=zh; ttwid=1%7CjG0F_7DNMfaP98zKWn7o1AkvrfZms1LZlSrYNlKFm7k%7C1735873856%7C536fc0aecffb670acb3f1d06af9f907074da4c598f5c8baf423017008d05543f; msToken=ZECxHUrsM-wpCzBzXY50Nmr6LfqynYsJIhZw1MbT41vf85sPRbhc49uHv84hJxP5G_YdXJFou3DNhFDIzEdVrVpPekokd2qMclth2JYpNidx96yMgyPuY2z31PoDkvpyPweIip_1"
}

# 发送请求
response = requests.get(url, headers=headers)

# 检查响应状态
if response.status_code == 200:
    data = response.json()
    # 提取关键词
    keywords = [item['keyword'] for item in data.get('data', {}).get('keyword_list', [])]

    # 保存到文件
    file_path = r"E:\tmp\社媒相关\搜索词.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        for keyword in keywords:
            file.write(keyword + "\n")

    print(f"关键词已保存到 {file_path}")
else:
    print(f"请求失败，状态码：{response.status_code}")
