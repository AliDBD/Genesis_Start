#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/3 11:28
# @Author : Genesis Ai
# @File : init_driver.py

from appium import webdriver
import time

def init_driver(udid, port):
    """
    初始化 Appium 驱动
    """
    desired_caps = {
        "platformName": "Android",
        "deviceName": udid,
        "udid": udid,
        "appPackage": "com.tencent.mm",
        "appActivity": ".ui.LauncherUI",
        "noReset": True
    }
    driver = webdriver.Remote(f"http://127.0.0.1:{port}/wd/hub", desired_caps)
    return driver

def tap_with_appium(driver, x, y):
    """
    使用现代化 Appium API 在屏幕上执行点击操作
    """
    driver.execute_script("mobile: tap", {"x": x, "y": y})
    print(f"Tapped at ({x}, {y})")

def perform_operations(udid, port):
    """
    对指定设备执行一系列操作
    """
    driver = init_driver(udid, port)
    try:
        print(f"Device {udid}: App launched, waiting for UI to load...")
        time.sleep(5)  # 等待 APP 加载

        # 点击目标坐标
        tap_with_appium(driver, 500, 1000)  # 替换为目标坐标
        print(f"Device {udid}: Operations completed.")
    except Exception as e:
        print(f"Error on device {udid}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    udid = "4b3b4c62"  # 替换为您的设备号
    port = 4723        # Appium 服务端口
    perform_operations(udid, port)


