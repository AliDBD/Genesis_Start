#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/20 16:57
# @Author : Genesis Ai
# @File : input_ider.py


with True:
    user_input = input("请输入关键字：")
    check = input(f"输入的值为:{user_input},确认输入Y，重新输入输入N")
    if check == "Y":
        print(f"已确认输入的关键字为：{user_input}")

    elif check == "N":
        print("请重新输入！")
    else:
        print(f"输入的值无效：{check}")