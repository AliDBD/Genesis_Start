#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/8 14:06

# @Author : linjingyu

# @File : htmlui.py
import re
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

# los = webdriver.Chrome()
# los.maximize_window()
# los.get("https://www.vct234.com/html/1/")
# los.add_cookie({"name":"Cookie","value":"abRequestId=c64382cd-b627-5cbe-82c2-cee36cf0871c; webId=8cc3af55dd44a76778cda2add0cfd88f; gid=yYS4J2dfYYjjyYS4J2df2f97Y2Mqx0EfWFhCEWxMqVC7j428DYUEdJ888J48qWY884yi00d8; cache_feeds=[]; a1=18c425ed585s3hawd7rvxs3jxu9b8pwe9dw42tu7h50000240378; web_session=040069b40565bb23e6f3b93a44374b88a9abfc; webBuild=3.19.3; unread={%22ub%22:%22656d95f3000000000801fb70%22%2C%22ue%22:%22655735c40000000032036685%22%2C%22uc%22:29}; xsecappid=xhs-pc-web; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=47587f18-a970-47a1-a81f-2d21c0ec49bb"}
# )
#
# time.sleep(5)
def movie():
    url = 'https://www.60b04.com/movie/wuma'

    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)
    return response.text

def loading():
    url = 'https://www.60b04.com/html/202312/79999.html'
    response = requests.get(url)
    if response.status_code == 200:
        html_data = response.text
        soup = BeautifulSoup(html_data,'html5lib')
        mp4_links = []
        for tag in soup.find_all(True):
            if 'value' in tag.attrs:
                value = tag['value']
                if re.match(r'.*\.mp4$',value):
                    mp4_links.append(value)
        for link in mp4_links:
            print(link)

    return link
loading()