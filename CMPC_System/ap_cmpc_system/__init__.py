#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/3 11:18
# @Author : Genesis Ai
# @File : __init__.py.py
'''
获取坐标
'''
from appium import webdriver

def init_driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "device",  # 替换为您的设备名称
        "udid": "4b3b4c62",      # 替换为您的设备ID
        "appPackage": "com.tencent.mm",  # 替换为目标APP包名
        "appActivity": ".ui.LauncherUI", # 替换为目标APP启动活动
        "noReset": True
    }

    print("Connecting to Appium server at: http://127.0.0.1:4723/wd/hub")
    print("Desired Capabilities:", desired_caps)

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723/wd/hub",
        desired_capabilities=desired_caps
    )
    print("Driver initialized successfully!")
    driver.quit()

init_driver()
