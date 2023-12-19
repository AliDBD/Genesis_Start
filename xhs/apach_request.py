#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/12/14 17:43
# @Author : Genesis Ai
# @File : data_request.py

import json
import pandas as pd
import time
import requests
import random
from bs4 import BeautifulSoup
from xhs.DB_Connect import save_id
from xhs.DB_Connect import save_data
from xhs.DB_Connect import find_id


class DoressData:

    #解析JSON数据获取定向ID值
    @staticmethod
    def extract_ids_to_excel(json_file_path):
        # 加载 JSON 数据
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        # 检查 'data' 和 'items' 键是否存在，并从中提取 IDs
        if 'data' in json_data and 'items' in json_data['data'] and isinstance(json_data['data']['items'], list):
            ids = [item['id'] for item in json_data['data']['items']]
        else:
            ids = []
        # # 将 IDs 保存到 DataFrame 中
        # df = pd.DataFrame(ids,columns=['ID'])
        # #, columns=['ID']
        #
        # # 将 DataFrame 保存到 Excel 文件中
        # df.to_excel(excel_file_path, index=False)
        # print(f"成功提取了 {len(ids)} 个 ID，并保存到了 '{excel_file_path}'。")
        # # 保存到 Excel...
        save_id(ids)

    #处理根据ID请求结果的html内容并解析数据
    @staticmethod
    def parse_html(html_data):
        soup = BeautifulSoup(html_data, 'html.parser')

        # 提取keywords和description
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords is not None:
            keywords = keywords['content']
        else:
            keywords = ""
        description = soup.find('meta', attrs={'name': 'description'})
        if description is not None:
            description = description['content']
        else:
            description = ""

        # 提取og:image
        og_images = soup.find_all('meta', attrs={'name': 'og:image'})
        og_image_values = [img['content'] for img in og_images]

        return keywords, description, og_image_values

    def found_data(self):
        # 读取 Excel 文件中的数据，获取 ID
        # excel_path = r'E:\2023年\spider\search_id.xlsx'
        # seach_id = pd.read_excel(excel_path)['ID']
        #从数据库获取id信息
        search_id = find_id()
        time_code = random.randint(2, 5)
        # 定义请求的 URL 和 headers
        url = "https://www.xiaohongshu.com/explore/"
        headers = {
            'User-Agent': 'AMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Host': 'www.xiaohongshu.com',
            'Connection': 'keep-alive'
        }
        # 创建一个空列表来存储请求结果
        results = []
        # 遍历 Excel 文件中的 ID，发送请求并处理响应
        for keywords in search_id():
            print(f"请求ID：{keywords}")
            time.sleep(time_code)
            username = 't17037773479161'
            password = 'lhlnpdmj'
            proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
            response = requests.get(url + keywords, headers=headers, proxies={'http': proxy, 'https': proxy})
            if response.status_code == 200:
                html_data = response.text
                keywords, description, og_images = DoressData.parse_html(html_data)
                save_data(keywords, description, og_images)
                #print(response.text)
                # 将提取的数据添加到结果列表中
                results.append({'标签': keywords, '文案内容': description,
                                **{f'og:image{i + 1}': img for i, img in enumerate(og_images)}})
                print(f"响应内容：\n{html_data}\n")
            else:
                print(f"请求 {keywords} 失败，状态码： {response.status_code}")
        # 将结果列表返回
        return results

def main():
    json_file_path = 'E:\\2023年\\spider\\json.txt'
    excel_file_path = 'E:\\2023年\\spider\\search_id.xlsx'
    #创建一个实例
    doress_data = DoressData()
    doress_data.extract_ids_to_excel(json_file_path,excel_file_path)
    #获取数据并处理
    data_list = doress_data.found_data()
    df = pd.DataFrame(data_list)
    df.to_excel('E:\\2023年\\spider\\temp_data.xlsx', index=False)


if __name__ == '__main__':
    main()
