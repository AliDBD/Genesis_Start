#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/2 11:55
# @Author : Genesis Ai
# @File : get_connected_devices.py

import subprocess

def get_connected_devices():
    """
    获取已连接的设备列表。
    """
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if 'device' in line]
    return devices

# 测试代码
devices = get_connected_devices()
if devices:
    print(f"Connected devices: {devices}")
else:
    print("No devices connected.")
