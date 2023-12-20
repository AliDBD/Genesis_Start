#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/20 16:38
# @Author : Genesis Ai
# @File : test.py

from bs4 import BeautifulSoup

def extract_all_card_feed_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取所有class="card-wrap"的<div>标签
    card_wraps = soup.find_all("div", class_="card-wrap")

    # 对于每个card-wrap，提取内部的card-feed中的所有文本
    extracted_texts = []
    for card in card_wraps:
        card_feed = card.find("div", class_="card-feed")
        if card_feed:
            text = card_feed.get_text(strip=True)
            extracted_texts.append(text)

    return extracted_texts

# 调用函数
json_file_path = 'E:\\2023年\\spider\\html.txt'
extracted_texts = extract_all_card_feed_text(json_file_path)

# 打印提取的文本
i = 0
for text in extracted_texts:
    i+=1
    print(f"第{i}个内容：{text}")


# 打印提取出的值
# for value in extracted_values:
#     print(value)
