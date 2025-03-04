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
            'profile': '喜欢搞笑视频',
            'content': '',
            'attachments': [base64_data]
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{udid}] API请求失败: {e}")
        return None


def send_comments_to_api(comments, udid, api_url):
    """
    发送前两条评论到API
    """
    try:
        if len(comments) >= 5:
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'profile': '喜欢搞笑视频',
                'content': comments[0],  # 主题
                'comments': comments[1] + comments[2] + comments[3] + comments[4]   # 评论内容
            }
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"[{udid}] 评论接口请求数据发送成功: {comments[0]}, {comments[1]}")
            return response.json()
    except Exception as e:
        print(f"[{udid}] 发送评论失败: {e}")
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
        x1, y1 = 683, 2046
        print(f"[{udid}] 准备点击第一个坐标: ({x1}, {y1})")
        tap_point(udid, x1, y1)

        # 等待页面响应和加载
        time.sleep(3)  # 根据实际情况调整等待时间

        # 第二个点击位置
        coordinate_list = [
            (900,507),
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
        time.sleep(5)
        #随机滑动次数
        # slide = random.randint(25, 300)
        # print(f"随机次数为：{slide}")
        slide =5
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
                    # 发送到API，设置超时时间为10秒
                    api_response = send_screenshot_to_api(base64_data, udid, api_url)
                    print(f"[{udid}] API返回: {api_response}")
                    
                    # 基础等待时间
                    base_wait_time = 2
                    
                    # 根据API返回结果中的isInterested值决定操作
                    if api_response and isinstance(api_response, dict) and api_response.get('isInterested') == True:
                        # 点击评论按钮
                        comment_list = [(970,2085),(1000,2085),(1030,2085),(1060,2085),(1090,2085)]
                        comment_x,comment_y = random.choice(comment_list)
                        print(f"[{udid}] 准备点击评论坐标: ({comment_x}, {comment_y})")
                        tap_point(udid, comment_x, comment_y)
                        
                        # 等待评论区加载
                        time.sleep(2)
                        
                        # 获取评论内容
                        comments = get_comments_ui(udid)
                        if comments:
                            print(f"[{udid}] 获取到的评论内容:")
                            for i, comment in enumerate(comments, 1):
                                print(f"{i}. {comment}")
                            
                            # 发送前两条评论到API
                            comments_api_url = "https://iris.iigood.com/iris/v1/agent/comment"
                            comments_response = send_comments_to_api(comments, udid, comments_api_url)
                            if comments_response:
                                print(f"[{udid}] 评论API返回: {comments_response}")
                        
                        # 随机决定上下滑动次数
                        up_swipes = random.randint(2, 5)
                        down_swipes = random.randint(1, 3)
                        print(f"[{udid}] 准备在评论区滑动: 向上{up_swipes}次, 向下{down_swipes}次")
                        
                        # 在评论区滑动
                        for _ in range(up_swipes):
                            subprocess.run(
                                ['adb', '-s', udid, 'shell', 'input', 'swipe', 
                                 '540', '1800', '540', '1000', '200'],
                                check=True, timeout=5
                            )
                            time.sleep(random.uniform(0.5, 3))
                        
                        for _ in range(down_swipes):
                            subprocess.run(
                                ['adb', '-s', udid, 'shell', 'input', 'swipe',
                                 '540', '1000', '540', '1800', '200'],
                                check=True, timeout=5
                            )
                            time.sleep(random.uniform(0.5, 3))
                        
                        # 关闭评论区
                        tap_point(udid, 540, 500)
                        time.sleep(1)
                        
                        # 计算并执行总等待时间
                        extra_wait_time = random.randint(1, 60)
                        total_wait_time = base_wait_time + extra_wait_time
                        print(f"[{udid}] isInterested为True，等待{total_wait_time}秒")
                        time.sleep(total_wait_time)
                    
                    else:
                        print(f"[{udid}] isInterested为False，等待{base_wait_time}秒")
                        time.sleep(base_wait_time)
                    
                    # 最后执行视频滑动
                    subprocess.run(
                        ['adb', '-s', udid, 'shell', 'input', 'swipe', '540', '2000', '540', '1000', '200'],
                        check=True, timeout=5
                    )
            except Exception as e:
                print(f"[{udid}] 操作发生错误: {e}")
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


def get_comments_accessibility(udid):
    """
    使用无障碍服务获取评论内容
    """
    try:
        result = subprocess.run([
            'adb', '-s', udid, 'shell', 'service', 'call', 'accessibility', '1'
        ], stdout=subprocess.PIPE, text=True)
        
        # 解析输出获取评论内容
        # 这部分需要根据实际的输出格式来实现
        
        return []
    except Exception as e:
        print(f"[{udid}] 通过无障碍服务获取评论失败: {e}")
        return []


def get_comments_ui(udid):
    """
    使用UIAutomator获取评论区的评论内容，只保留8个字以上的评论
    """
    try:
        print(f"[{udid}] 开始获取评论内容...")
        
        # 使用UIAutomator dump当前界面
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # 等待文件生成
        time.sleep(1)
        
        # 将xml文件拉到本地
        subprocess.run(
            ['adb', '-s', udid, 'pull', '/data/local/tmp/ui.xml', f'comments_{udid}.xml'],
            check=True
        )
        
        # 读取xml文件内容
        import xml.etree.ElementTree as ET
        tree = ET.parse(f'comments_{udid}.xml')
        root = tree.getroot()
        
        # 接收评论内容
        comments = []
        # 根据特定的TextView特征来识别评论
        for node in root.findall(".//node[@class='android.widget.TextView']"):
            text = node.get('text', '').strip()
            # 过滤条件：长度大于8且不以特定文字开头
            if text and len(text) >= 8 and not text.startswith(('点赞', '评论', '分享')):
                comments.append(text)
        
        # 清理临时文件
        os.remove(f'comments_{udid}.xml')
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        
        print(f"[{udid}] 获取到{len(comments)}条8字以上的评论")
        return comments
        
    except Exception as e:
        print(f"[{udid}] 获取评论失败: {e}")
        # 清理可能存在的临时文件
        try:
            if os.path.exists(f'comments_{udid}.xml'):
                os.remove(f'comments_{udid}.xml')
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        except:
            pass
        return []


if __name__ == "__main__":
    main()

