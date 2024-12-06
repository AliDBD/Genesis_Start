#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/3 10:53
# @Author : Genesis Ai
# @File : init_driver.py

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

def init_driver(udid):
    capabilities = {
        "platformName": "Android",
        "deviceName": udid,
        "udid": udid,
        "appPackage": "com.tencent.mm",
        "appActivity": ".ui.LauncherUI",
        "noReset": True
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
    return driver

def tap_with_appium(driver, x, y):
    action = TouchAction(driver)
    action.tap(x=x, y=y).perform()

def perform_operations(udid):
    driver = init_driver(udid)
    time.sleep(5)  # 等待APP加载
    tap_with_appium(driver, 680, 2232)  # 替换为目标坐标
    driver.quit()
