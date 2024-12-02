#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/26 下午3:59
# @Author : Genesis Ai
# @File : 风力发电叶尖速度计算.py

import math

# 扇叶半径（米）
radius = 50  # 假设半径为50米

# 扇叶转速（转每分钟）
RPM = 20  # 假设转速为20 RPM

# 计算叶尖的线速度（米/秒）
linear_velocity_m_per_s = 2 * math.pi * radius * (RPM / 60)

# 转换为公里/小时
linear_velocity_km_per_h = linear_velocity_m_per_s * 3.6

print(f"叶尖的线速度是 {linear_velocity_m_per_s:.2f} 米/秒")
print(f"叶尖的线速度是 {linear_velocity_km_per_h:.2f} 公里/小时")
