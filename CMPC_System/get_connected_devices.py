#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/12/2 11:55
# @Author : Genesis Ai
# @File : get_connected_devices.py
'''
**可以获取设备号
**可以打开微信，获取坐标
'''

import subprocess
import threading
import time
import logging
import random
import base64
import requests
import os
from datetime import datetime

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")


def get_connected_devices():
    """
    获取已连接的设备列表。
    """
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if 'device' in line]
    return devices


def is_screen_on(udid):
    """
    检查屏幕是否亮起。
    """
    result = subprocess.run(['adb', '-s', udid, 'shell', 'dumpsys', 'power'], stdout=subprocess.PIPE, text=True)
    return "state=ON" in result.stdout


def unlock_screen(udid):
    """
    解锁设备屏幕（适用于无密码锁屏）。
    """
    print(f"[{udid}] 正在解锁屏幕")
    subprocess.run(['adb', '-s', udid, 'shell', 'input', 'swipe', '540', '2000', '540', '800'])
    time.sleep(2)
    if is_screen_on(udid):
        print(f"[{udid}] 屏幕已解锁")
    else:
        print(f"[{udid}] 无法解锁屏幕")


def ensure_screen_unlocked(udid):
    """
    确保屏幕被唤醒并解锁。
    """
    if not is_screen_on(udid):
        print(f"[{udid}] 屏幕关闭，正在唤醒")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
        time.sleep(1)
    unlock_screen(udid)


# def ensure_screen_unlocked(udid):
#     """
#     确保屏幕被唤醒并解锁。
#     """
#     if not is_screen_on(udid):  # 检查屏幕是否亮起
#         print(f"[{udid}] 屏幕关闭，正在唤醒")
#         subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
#         time.sleep(1)
#
#     if not is_screen_on(udid):  # 再次确认屏幕状态
#         print(f"[{udid}] 屏幕仍未唤醒，放弃解锁")
#         return  # 如果屏幕仍然关闭，直接返回
#
#     unlock_screen(udid)  # 解锁屏幕


def get_screen_size(udid):
    """
    获取设备的屏幕分辨率。
    """
    ensure_screen_unlocked(udid)
    result = subprocess.run(['adb', '-s', udid, 'shell', 'wm', 'size'], stdout=subprocess.PIPE, text=True)
    size_lines = result.stdout.strip().split('\n')

    # 遍历所有行，查找包含 "Physical size" 的行
    for line in size_lines:
        if "Physical size" in line:
            size = line.split(":")[1].strip()
            width, height = map(int, size.split("x"))
            print(f"[{udid}] 屏幕尺寸: {width}x{height}")
            return width, height

    # 如果没有找到 Physical size，尝试使用第一行
    try:
        size = size_lines[0].strip()
        width, height = map(int, size.split("x"))
        print(f"[{udid}] 屏幕尺寸: {width}x{height}")
        return width, height
    except Exception as e:
        print(f"[{udid}] 无法获取屏幕尺寸: {e}")
        return None, None


# def calculate_tap_point(screen_width, screen_height, x_ratio, y_ratio):
#     """
#     根据屏幕分辨率和比例计算点击点的绝对坐标。
#     """
#     x = int(screen_width * x_ratio)
#     y = int(screen_height * y_ratio)
#     # 添加边界检查
#     if x <= 0 or x >= screen_width or y <= 0 or y >= screen_height:
#         print(f"计算的坐标点 ({x}, {y}) 超出屏幕范围")
#         return None, None
#     print(f"计算点击点: ({x}, {y})")
#     return x, y


def open_app(udid, package_name):
    """
    打开指定设备上的指定APP。
    """
    print(f"[{udid}] 正在打开应用: {package_name}")
    subprocess.run(['adb', '-s', udid, 'shell', 'am', 'start', '-n', package_name])


def tap_point(udid, x, y):
    """
    在指定设备上的指定坐标执行点击操作。
    添加点击验证和重试机制
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[{udid}] 尝试第{attempt + 1}次点击坐标 ({x}, {y})")
            subprocess.run(['adb', '-s', udid, 'shell', 'input', 'tap', str(x), str(y)],
                           check=True)  # 添加check=True来检查命令是否成功
            time.sleep(1)  # 等待点击响应
            return True
        except subprocess.CalledProcessError as e:
            print(f"[{udid}] 点击失败: {e}")
            if attempt == max_retries - 1:
                return False
            time.sleep(1)


def force_stop_app(udid, package_name):
    """
    强制停止应用
    """
    package_name = package_name.split('/')[0]
    print(f"[{udid}] 强制停止应用: {package_name}")
    subprocess.run(['adb', '-s', udid, 'shell', 'am', 'force-stop', package_name])


def check_device_connected(udid):
    """
    检查设备是否仍然连接
    """
    try:
        result = subprocess.run(['adb', '-s', udid, 'get-state'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        return 'device' in result.stdout
    except:
        return False


def get_screenshot_base64(udid):
    """
    获取设备截图并转换为base64，确保每次都是最新的截图
    """
    try:
        print(f"[{udid}] 开始执行截屏操作...")
        
        # 清理设备上可能存在的旧截图
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'], check=True)
        print(f"[{udid}] 已清理旧截图")
        
        # 生成带时间戳的文件名，确保唯一性
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        device_filename = f"/data/local/tmp/screen_{timestamp}.png"
        local_filename = f"temp_{udid}_{timestamp}.png"
        
        # 截取新图片
        print(f"[{udid}] 正在截取屏幕...")
        subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', device_filename], check=True)
        print(f"[{udid}] 截图已保存到设备: {device_filename}")
        
        # 将截图从设备拉取到本地
        print(f"[{udid}] 正在将截图传输到本地...")
        subprocess.run(['adb', '-s', udid, 'pull', device_filename, local_filename], check=True)
        print(f"[{udid}] 截图已保存到本地: {local_filename}")
        
        # 读取图片并转换为base64
        print(f"[{udid}] 正在转换图片为base64...")
        with open(local_filename, 'rb') as image_file:
            # 直接读取二进制数据
            image_binary = image_file.read()
            # 转换为base64，并确保输出是字符串
            base64_data = base64.b64encode(image_binary).decode('utf-8')
        print(f"[{udid}] 图片已成功转换为base64")
        
        # 清理临时文件
        os.remove(local_filename)
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', device_filename], check=True)
        print(f"[{udid}] 临时文件已清理")
        
        # 不要打印完整的base64字符串，太长了
        print(f"[{udid}] Base64长度: {len(base64_data)}")
        
        return base64_data
    except Exception as e:
        print(f"[{udid}] 截图失败: {e}")
        # 发生错误时也要尝试清理临时文件
        try:
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'])
            for temp_file in os.listdir('.'):
                if temp_file.startswith(f'temp_{udid}_') and temp_file.endswith('.png'):
                    os.remove(temp_file)
        except:
            pass
        return None


def send_screenshot_to_api(base64_data, udid, api_url):
    """
    发送base64图片数据到API
    """
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        # 确保base64数据格式正确
        if not base64_data.startswith('data:image/'):
            base64_data = f"data:image/png;base64,{base64_data}"
            
        payload = {
            'profile': '喜欢搞笑视频、喜欢汽车类',
            'content': '',
            'attachments': [base64_data]
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{udid}] API请求失败: {e}")
        return None


def perform_operations(udid):
    try:
        print(f"[{udid}] 开始执行操作")

        # 确保屏幕解锁
        ensure_screen_unlocked(udid)

        # 先强制停止微信
        force_stop_app(udid, "com.tencent.mm/com.tencent.mm.ui.LauncherUI")
        time.sleep(2)

        # 重新打开应用
        open_app(udid, "com.tencent.mm/com.tencent.mm.ui.LauncherUI")

        # 等待应用加载
        time.sleep(6)

        # 获取屏幕分辨率
        screen_width, screen_height = get_screen_size(udid)
        if not screen_width or not screen_height:
            print(f"[{udid}] 无法获取屏幕尺寸")
            return

        # 第一个点击位置
        x1, y1 = 686, 2187
        print(f"[{udid}] 准备点击第一个坐标: ({x1}, {y1})")
        tap_point(udid, x1, y1)

        # 等待页面响应和加载
        time.sleep(5)  # 根据实际情况调整等待时间

        # 第二个点击位置
        coordinate_list = [
            (966,507),
            (220,430),
            (250,530),
            (255,540),
            (480,490),
            (760,515),
            (855,508)
        ]
        x2, y2 = random.choice(coordinate_list)
        print(f"[{udid}] 准备点击第二个坐标: ({x2}, {y2})")
        tap_point(udid, x2, y2)

        #随机滑动次数
        #slide = random.randint(25, 300)
        slide =5
        time.sleep(5)
        # 设置API地址
        api_url = "https://iris.iigood.com/iris/v1/agent/interest"
        for i in range(slide):
            # 检查设备是否仍然连接
            if not check_device_connected(udid):
                print(f"[{udid}] 设备已断开连接，停止操作")
                return
                
            print(f"第{i+1}次滑动操作")
            try:
                # 获取截图并转换为base64
                base64_data = get_screenshot_base64(udid)
                if base64_data:
                    try:
                        # 发送到API，设置超时时间为10秒
                        api_response = send_screenshot_to_api(base64_data, udid, api_url)
                        print(f"[{udid}] API返回: {api_response}")
                        
                        # 如果API请求成功，根据返回值处理
                        if api_response and isinstance(api_response, dict):
                            # 基础等待时间
                            base_wait_time = 2
                            # 根据API返回结果中的isInterested值决定额外等待时间
                            if api_response.get('isInterested') == True:
                                extra_wait_time = random.randint(1, 60)
                                total_wait_time = base_wait_time + extra_wait_time
                                click_time = random.randint(3,total_wait_time)
                                click_wait_time = random.randint(3,total_wait_time)
                                
                                # 随机获取坐标列表的坐标进行点击评论按钮
                                comment_list = [(970,2085),(1000,2085),(1030,2085),(1060,2085),(1090,2085)]
                                comment_x,comment_y = random.choice(comment_list)
                                print(f"[{udid}] 准备点击评论坐标: ({comment_x}, {comment_y})")
                                tap_point(udid, comment_x, comment_y)
                                
                                # 等待评论区加载
                                time.sleep(2)
                                
                                # 随机决定上下滑动次数
                                up_swipes = random.randint(2, 5)    # 向上滑动2-5次
                                down_swipes = random.randint(1, 3)  # 向下滑动1-3次
                                
                                print(f"[{udid}] 准备在评论区滑动: 向上{up_swipes}次, 向下{down_swipes}次")
                                
                                # 先向上滑动
                                for _ in range(up_swipes):
                                    try:
                                        # 在评论区范围内滑动（Y坐标范围根据实际评论区位置调整）
                                        subprocess.run(
                                            ['adb', '-s', udid, 'shell', 'input', 'swipe', 
                                             '540', '1800', '540', '1000', '200'],
                                            check=True, timeout=5
                                        )
                                        # 每次滑动后短暂等待
                                        time.sleep(random.uniform(0.5, 3))
                                    except Exception as e:
                                        print(f"[{udid}] 评论区向上滑动失败: {e}")
                                
                                # 然后向下滑动
                                for _ in range(down_swipes):
                                    try:
                                        subprocess.run(
                                            ['adb', '-s', udid, 'shell', 'input', 'swipe',
                                             '540', '1000', '540', '1800', '200'],
                                            check=True, timeout=5
                                        )
                                        # 每次滑动后短暂等待
                                        time.sleep(random.uniform(0.5, 3))
                                    except Exception as e:
                                        print(f"[{udid}] 评论区向下滑动失败: {e}")
                                
                                # 点击顶部空白区域关闭评论区
                                tap_point(udid, 540, 500)
                                time.sleep(1)
                                
                                print(f"[{udid}] isInterested为True，基础等待{base_wait_time}秒 + 随机等待{extra_wait_time}秒 = 总共等待{total_wait_time}秒")
                            else:
                                total_wait_time = base_wait_time
                                print(f"[{udid}] isInterested为False，等待{total_wait_time}秒")
                        else:
                            # API请求失败或返回格式不正确，使用默认等待时间
                            total_wait_time = 2
                            print(f"[{udid}] API返回异常，使用默认等待时间{total_wait_time}秒")
                            
                    except Exception as api_error:
                        # API请求出错，使用默认等待时间
                        total_wait_time = 2
                        print(f"[{udid}] API请求失败: {api_error}，使用默认等待时间{total_wait_time}秒")
                    
                    # 执行等待
                    time.sleep(total_wait_time)
                else:
                    # 截图失败，使用默认等待时间
                    print(f"[{udid}] 截图失败，使用默认等待时间2秒")
                    time.sleep(2)
                
                # 执行滑动操作
                result = subprocess.run(
                    ['adb', '-s', udid, 'shell', 'input', 'swipe', '540', '2000', '540', '1000', '200'],
                    check=True,  
                    timeout=5    
                )
            except subprocess.TimeoutExpired:
                print(f"[{udid}] 滑动操作超时，设备可能已断开")
                return
            except subprocess.CalledProcessError:
                print(f"[{udid}] 滑动操作失败，设备可能已断开")
                return
            except Exception as e:
                print(f"[{udid}] 滑动操作发生错误: {e}")
                return

        print(f"[{udid}] 操作完成")
    except Exception as e:
        print(f"[{udid}] 操作时发生错误: {e}")


def lock_screen(udid):
    """
    锁定设备屏幕
    """
    try:
        print(f"[{udid}] 正在锁定屏幕...")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_POWER'], check=True)
        print(f"[{udid}] 屏幕已锁定")
    except Exception as e:
        print(f"[{udid}] 锁屏失败: {e}")


def main():
    """
    主程序入口。
    """
    devices = get_connected_devices()
    if not devices:
        print("没有检测到连接的设备")
        return

    print(f"检测到的设备: {devices}")

    # 多线程执行操作
    threads = []
    for udid in devices:
        thread = threading.Thread(target=perform_operations, args=(udid,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("所有设备操作完成")
    
    # 所有设备操作完成后，关闭APP并锁屏
    for udid in devices:
        try:
            # 强制停止微信
            force_stop_app(udid, "com.tencent.mm/com.tencent.mm.ui.LauncherUI")
            print(f"[{udid}] 微信已关闭")
            
            # 等待一下确保APP完全关闭
            time.sleep(2)
            
            # 锁定屏幕
            lock_screen(udid)
            
        except Exception as e:
            print(f"[{udid}] 关闭APP或锁屏时发生错误: {e}")

    print("所有设备已关闭APP并锁屏")


if __name__ == "__main__":
    main()

