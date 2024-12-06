#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/3 10:37
# @Author : Genesis Ai
# @File : get_screen_size.py
'''
获取屏幕信息
'''
import subprocess


def get_screen_size(udid):
    """
    获取设备屏幕分辨率。
    """
    result = subprocess.run(['adb', '-s', udid, 'shell', 'wm', 'size'], stdout=subprocess.PIPE, text=True)
    size_line = result.stdout.strip()
    if "Physical size" in size_line:
        size = size_line.split(":")[1].strip()
        width, height = map(int, size.split("x"))
        return width, height
    return None, None

def calculate_tap_point(screen_width, screen_height, x_ratio, y_ratio):
    """
    根据分辨率计算点击点坐标。
    """
    x = int(screen_width * x_ratio)
    y = int(screen_height * y_ratio)
    return x, y
