#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/4/10 16:47
# @Author : Genesis Ai
# @File : 装饰器示例.py

def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before calling the function")
        result = func(*args, **kwargs) #调用原始函数,并传递任意参数
        print("After calling the function")
        return result
    return wrapper

@decorator
def add(x,y):
    return x+y

print(add(2,3))


# def decorator(func):
#     def wrapper(*args, **kwargs):
#         print("Before calling the function")
#         result = func(*args, **kwargs)  # 调用原始函数，并传递任意参数
#         print("After calling the function")
#         return result  # 返回原始函数的返回值
#     return wrapper
#
# @decorator
# def add(x, y):
#     return x + y
#
# print(add(2, 3))
