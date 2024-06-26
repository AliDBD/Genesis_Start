#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/13 14:31
# @Author : Genesis Ai
# @File : web_driver_project.py
'''
# 本地实际chromedriver路径
chrome_driver_path = 'D:/Software Tool/pyhton3.10/chromedriver.exe'
'''

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# HTML内容
html_content = '''<body class="file_link_main">
<div class="header_block">
    <div class="public_header">
        ...
        <tbody>
            <tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-1【2022】【六下】【拱墅区】【分班考】【语文】解析.pdf" ...></tr>
            <tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-2【2022】【六下】【拱墅区】【分班考】【数学】解析.pdf" ...></tr>
            <tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-3【2022】【六下】【拱墅区】【分班考】【英语】解析.pdf" ...></tr>
            <tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-4【2022】【六下】【拱墅区】【分班考】【科学】解析.pdf" ...></tr>
            ...
        </tbody>
        ...
</body>'''

# 解析HTML
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
tbody = soup.find('tbody')

# 提取文件名
filenames = [tr['data-filename'] for tr in tbody.find_all('tr', class_='file_item')]

# 基础URL
base_url = 'https://yk3.gokuai.com/file/lbmro9nvmfw0c6f807bitgcktdcgaz60#!::'

# 保存PDF文件的目录
save_dir = 'downloaded_pdfs'

# 如果目录不存在，则创建目录
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# ChromeDriver路径
chrome_driver_path = 'D:/Software Tool/pyhton3.10/chromedriver.exe'

# 设置Selenium WebDriver（使用Chrome）
options = Options()
options.add_experimental_option('prefs', {
    "download.default_directory": os.path.abspath(save_dir),  # 设置默认下载目录
    "download.prompt_for_download": False,  # 下载时不提示
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # 不使用Chrome内置的PDF查看器
})
options.headless = False  # 无头模式运行（不打开浏览器窗口）
service = Service(executable_path=chrome_driver_path)  # 指定chromedriver的路径
driver = webdriver.Chrome(service=service, options=options)


# 下载PDF文件的函数，使用Selenium模拟点击下载按钮
def download_pdf(pdf_url, filename):
    driver.get(pdf_url)
    time.sleep(25)  # 等待页面完全加载

    # 模拟滚动页面到底部，确保所有内容加载完毕
    scroll_pause_time = 25 # 设置每次滚动后等待的时间
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(5)  # 额外等待，确保所有内容加载完成

    # 查找并点击下载按钮
    try:
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cmd_link_download"))
        )
        download_button.click()
    except Exception as e:
        print(f"未找到下载按钮或下载失败: {e}")
        return False

    time.sleep(10)  # 等待下载完成

    # 检查文件是否已下载
    file_path = os.path.join(save_dir, filename)
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0


# 下载PDF文件
for filename in filenames:
    pdf_url = f'{base_url}{filename}:'
    print(f'正在下载 {pdf_url}')

    if download_pdf(pdf_url, filename):
        print(f'成功下载 {filename} 到 {save_dir}')
    else:
        print(f'下载 {filename} 失败')

driver.quit()
print('下载完成')
