#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/26 14:23
# @Author : Genesis Ai
# @File : cookie.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 1、加载数据
# data1 = pd.read_excel('E:\\2024\\Git_Bush\\sum_data.xlsx',sheet_name='waimao')
# data2 = pd.read_excel('E:\\2024\\Git_Bush\\temp_data.xlsx',sheet_name='Sheet1')
data3 = pd.read_excel('E:\\2024\\Git_Bush\\关键词点击率_2023060102.xlsx',sheet_name='1-关键词点击率')
#print(data1,data2)

# 2、数据预处理（NA空值处理）,分析数据
data = pd.concat([data3],axis=0)#按照行拼接数据
data.dropna(axis=1,inplace=True)
#data.head(5)
data.info()

#统计平均搜索率
mounta=round(data['搜索结果总数'].mean(),2)
print(f'搜索平均数：{mounta}')

#频数统计，什么词出现率最高
dishes_count = data['关键词'].value_counts()[:10]
print(dishes_count)
# 3、数据可视化matplotlib
dishes_count.plot(kind='bar')
