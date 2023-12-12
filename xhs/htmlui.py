#!/usr/bin/env python

# -- coding: utf-8 --

# @Time : 2023/12/8 15:45

# @Author : linjingyu

# @File : htmlui.py

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


#获取本地id
def red_excel():
    # 指定文件路径
    file_path = r'E:\2023年\十二月\data.xlsx'
    # 读取Excel文件
    data = pd.read_excel(file_path, skiprows=range(1), engine='openpyxl')
    data_list = data.values.tolist()
    # 打印数据
    print(data_list)
    return data_list

def arry_list(List):
    for id in List:
        print(id)


    pass

red_excel()