#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/8/6 10:59
# @Author : Genesis Ai
# @File : 20240806更新.py
#最新可用的定向爬取代码
'''
1、通过抓包的方法获取xhs站点的信息，接口返回数据v1/search/notes
2、将notes接口返回的数据通过json格式化，保存到本地的json文件夹
3、通过id提取脚本读取本地notesdata.json文件，将所需要的内容xsec_token、id提取出来并储存到本地excel文档
4、为了数据完整性，需要本地处理一下excel表格信息（此步骤可以忽略，方法可以集成到id提取脚本里面）
5、使用“获取ID储存到数据库”脚本，将所需要的xsec_token、id写入到数据库
6、运行此脚本，将会自动获取数据库的xsec_token、id，并将所需要的数据提取出来保存到xhs_json表
'''

import json
import pandas as pd
import time
import requests
import random
import re
import http.client
from bs4 import BeautifulSoup
from xhs.DB_Connect import save_id
from xhs.DB_Connect import save_data
from xhs.DB_Connect import find_id, find_userid
from xhs.DB_Connect import clear_disdata, synchronous_userid

class DoressData:
    @staticmethod
    def login_token():
        url = "https://testbuyerapi.chinagoods.com/v1/auth/login"

        headers = {
            # 'Host':'<calculated when request is sent>',
            'Content-Length': '<calculated when request is sent>',
            'Content-Type': 'application/json'
        }

        data = json.dumps({
            "grant_type": "password",
            "scope": "buyer",
            "username": "13408400153",
            "password": "abc123456"
        })

        response = requests.post(url=url, headers=headers, data=data)
        # 提取token
        json_data = json.loads(response.text)  # 将返回的json字符串转为字典
        token = re.search(r'"access_token":\s*"([^"]+)"', json.dumps(json_data)).group(1)
        print(f"返回的token信息：{token}")
        return token

    # 获取定向博主的首页内容（html源码）
    @staticmethod
    def ghome_html():
        url = 'https://www.xiaohongshu.com/explore/'
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': 'www.xiaohongshu.com',
            'Connection': 'keep-alive'
        }
        time_code = random.randint(2, 10)
        userid_list = find_userid()
        for row in userid_list:
            search_id = row['search_id']
            xsec_token = row['xsec_token']
            print(f"请求用户ID：{search_id},{xsec_token}")
            time.sleep(time_code)
            username = 't17037773479161'
            password = 'lhlnpdmj'
            proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
            response = requests.get(url=url + search_id + f'?xsec_token={xsec_token}&xsec_source=pc_search', headers=headers, proxies={'http': proxy, 'https': proxy})
            if response.status_code == 200:
                html_data = response.text
                print(f"返回数据体：{html_data}")
                DoressData.extract_noteIds(html_data, search_id)

    # 根据博主首页源码信息解析出当前首页的ID储存到库
    @staticmethod
    def extract_noteIds(file_path, user_id):
        print("html数据接收成功，开始解析ID***********！")
        soup = BeautifulSoup(file_path, 'html.parser')
        noteIds = []
        pattern = r'\"noteId\":\"([^\"]+)\"'
        time.sleep(8)
        matches = re.findall(pattern, str(soup))
        for match in matches:
            noteIds.append((match, user_id))
        # 获取到的ID去重
        unique_noteIds = list(set(noteIds))
        # 将数据保存至数据库
        save_id(unique_noteIds)
        print(f"解析结果ID储存到数据库完成！{unique_noteIds}")

    # 处理根据ID请求结果的html内容并解析数据
    @staticmethod
    def parse_html(html_data, token):
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
        meta_tags = soup.find_all('meta', {'name': 'og:image'})
        urls = [tag['content'] for tag in meta_tags if 'content' in tag.attrs]
        print(f"提取的图片地址：{urls}")

        # 调用url_list方法转换地址
        ret_og_image_values = DoressData.url_list(urls, token)
        print(f"提取的图片地址列表{ret_og_image_values}")

        return keywords, description, ret_og_image_values

    # 调用张均利接口处理image地址
    @staticmethod
    def url_list(urllist, token):
        formatted_list = []
        # 检查 urllist 是否为字符串
        if isinstance(urllist, str):
            urls = urllist.split(',')
        elif isinstance(urllist, list):
            urls = urllist
        else:
            # urllist 既不是字符串也不是列表
            raise ValueError("urllist must be either a string or a list")
        idrice = 0
        for url in urls:
            idrice += 1
            formatted_url = url.strip()
            print(f"开始转换第{idrice}个ULR请求转换：{url}")
            conn = http.client.HTTPSConnection("testapiserver.chinagoods.com")
            payload = json.dumps({
                "urlList": [formatted_url]
            })
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': 'uatapiserver.chinagoods.com',
                'Connection': 'keep-alive',
                'Authorization': f"Bearer {token}"
            }
            # print(f"接口URL转换请求链接：{urllist}")
            print(f"请求token：Bearer {token}")
            conn.request("POST", "/pms/user/v1/goods_pic/describe/change", payload, headers)
            res = conn.getresponse()
            data = res.read()
            source_url = data.decode('utf-8')
            parsed_json = json.loads(source_url)
            data_values = parsed_json.get('data', [])
            url = data_values[0] if data_values else None
            # 返回接口单个URL信息
            print(f"处理完成的URL：{res}")
            # 将转换结果的url储存到list
            if url:
                formatted_list.append(url)
        return formatted_list

    def found_data(self):
        # 从数据库获取id信息
        print("开始获取数据库动态ID！！！！！")
        # 获取Token
        token = DoressData.login_token()
        time_code = random.randint(2, 15)
        # 定义请求的 URL 和 headers
        url = "https://www.xiaohongshu.com/explore/"
        headers = {
            'User-Agent': 'AMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Host': 'www.xiaohongshu.com',
            'Connection': 'keep-alive'
        }

        results = []
        userid_list = find_userid()
        for row in userid_list:
            search_id = row['search_id']
            xsec_token = row['xsec_token']
            print(f"请求用户ID：{search_id},{xsec_token}")
            time.sleep(time_code)
            username = 't17037773479161'
            password = 'lhlnpdmj'
            proxy = f"http://{username}:{password}@d842.kdltps.com:15818"
            response = requests.get(url=url + search_id + f'?xsec_token={xsec_token}&xsec_source=pc_search',
                                    headers=headers, proxies={'http': proxy, 'https': proxy})
            print(f"请求的URL：{url + search_id + f'?xsec_token={xsec_token}&xsec_source=pc_search'}")
            if response.status_code == 200:
                html_data = response.text
                print(f"响应内容：\n{html_data}\n")
                keywords, description, ret_og_image_values = DoressData.parse_html(html_data, token)
                print(f"最终获取到要保存的数据：{keywords}, image: {ret_og_image_values}")
                # 将提取的数据添加到结果列表中
                results.append({'标签': keywords, '文案内容': description,
                                **{f'og:image{i + 1}': img for i, img in enumerate(ret_og_image_values)}, 'ID': search_id})
                save_data(keywords, description, ret_og_image_values, search_id)
            else:
                print(f"请求 {search_id} 失败，状态码： {response.status_code}")
            # 清除垃圾数据
            clear_disdata()
            # 调用synchronous_userid方法同步xhs_json表的user_id
            synchronous_userid()
        # 将结果列表返回
        return results

def main():
    # 创建一个实例
    doress_data = DoressData()
    # doress_data.ghome_html()
    # 获取数据并处理
    data_list = doress_data.found_data()
    df = pd.DataFrame(data_list)
    df.to_excel('E:\\2023年\\spider\\temp_data.xlsx', index=False)

if __name__ == '__main__':
    main()
