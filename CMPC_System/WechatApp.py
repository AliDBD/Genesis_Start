#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/12/9 11:55
# @Author : Genesis Ai
# @File : Multi-platform.py
'''
**可以获取设备号
**可以打开微信，获取坐标
**可以打开抖音，获取坐标
**可以发送图片到API
**可以发送评论到API 
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
from get_connected_devices import *  # 导入基础功能
import re
import sys
import locale

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")

# 添加设备信息缓存
device_info_cache = {}

# 在文件开头或函数之前定义completed_devices
completed_devices = []


def cache_device_info(udid):
    """
    缓存设备信息，包括屏幕尺寸和常用坐标
    """
    try:
        if udid not in device_info_cache:
            # 获取屏幕尺寸
            screen_width, screen_height = get_screen_size(udid)

            # 计算常用坐标
            device_info_cache[udid] = {
                'screen_width': screen_width,
                'screen_height': screen_height,
                'center_x': screen_width // 2,
                'center_y': screen_height // 2,
                'coordinates': {
                    'swipe_start': (540, 1800),
                    'swipe_end': (540, 500),
                    'comment_buttons': [(970, 2085), (1000, 2085), (1030, 2085), (1060, 2085), (1090, 2085)],
                    'close_comment': (540, 500)
                }
            }
            print(f"[{udid}] 设备信息已缓存")

        return device_info_cache[udid]
    except Exception as e:
        print(f"[{udid}] 缓存设备信息失败: {e}")
        return None


def get_connected_devices():
    """
    获取已连接的设备列表。
    """
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if 'device' in line]
    print(f"检测到的设备: {devices}")
    return devices


def is_screen_on(udid):
    """
    检查屏幕是否亮起，使用更可靠的检测方法
    """
    try:
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'dumpsys', 'display | grep "mScreenState"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        print(f"[{udid}] 屏幕状态检查结果: {result.stdout}")  # 添加调试信息
        return "ON" in result.stdout or "SCREEN_STATE_ON" in result.stdout
    except Exception as e:
        print(f"[{udid}] 检查屏幕状态时出错: {e}")
        return True  # 如果检查失败，默认认为屏幕是亮着的


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


def retry_operation(max_retries=3, delay=1):
    """
    重试装饰器，用于需要重试的操作
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"操作失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


@retry_operation(max_retries=3)
def tap_point(udid, x, y):
    """
    改进后的点击操作，添加重试机制
    """
    print(f"[{udid}] 点击坐标 ({x}, {y})")
    subprocess.run(['adb', '-s', udid, 'shell', 'input', 'tap', str(x), str(y)],
                   check=True)
    time.sleep(0.5)  # 等待点击响应
    return True


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
            'profile': '喜欢美妆和美女',
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
                'profile': '喜欢汽车美女',
                'content': comments[0],  # 主题
                'comments': comments[1] + comments[2] + comments[3] + comments[4]  # 评论内容
            }
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"[{udid}] 评论接口请求数据发送成功: {comments[0]}, {comments[1]}")
            return response.json()
    except Exception as e:
        print(f"[{udid}] 发送评论失败: {e}")
    return None


def perform_operations(udid):
    """
    微信视频号页面操作
    """
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

        # 检查微信登录状态
        if not check_wechat_login(udid):
            print(f"[{udid}] 微信未登录，跳过微信相关操作")
            # 强制停止微信
            force_stop_app(udid, "com.tencent.mm/com.tencent.mm.ui.LauncherUI")
            time.sleep(2)
            # 回到主屏幕
            subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
            time.sleep(2)
            print(f"[{udid}] 开始执行下一个应用的操作")
            # 继续执行抖音操作
            perform_douyin_operations(udid)
            return

        print(f"[{udid}] 微信已登录，继续执行微信操作")

        # 获取屏幕分辨率
        screen_width, screen_height = get_screen_size(udid)
        if not screen_width or not screen_height:
            print(f"[{udid}] 无法获取屏幕尺寸")
            return

        # 执行微信的其他操作...
        # 第一个点击位置
        x1, y1 = 686, 2187
        print(f"[{udid}] 准备点击第一个坐标发现位置: ({x1}, {y1})")
        tap_point(udid, x1, y1)
        # 等待页面响应和加载
        time.sleep(2)  # 根据实际情况调整等待时间
        # 视频号搜索按钮坐标
        coordinateone_list = [
            (880, 160),
            (880, 190),
            (890, 178),
            (892, 177),
            (889, 188),
            (901, 191),
            (899, 183),
        ]
        #确认搜索关键位置坐标
        search_list = [
            (960, 195),
            (961, 190),
            (957, 183),
            (958, 185),
            (950, 190),
            (955, 189),
            (957, 195),
        ]

        # 第二个点击位置
        coordinate_list = [
            (966, 507),
            (220, 430),
            (250, 530),
            (255, 540),
            (480, 490),
            (760, 515),
            (855, 508)
        ]
        x2, y2 = random.choice(coordinate_list)
        print(f"[{udid}] 准备点击第二个坐标视频号: ({x2}, {y2})")
        tap_point(udid, x2, y2)

        # 检查是否出现"我知道了"关键字
        time.sleep(5)
        if check_and_close_popup(udid, "我知道了"):
            print(f"[{udid}] 关闭了\"我知道了\"弹窗")

        new_x, new_y = random.choice(coordinateone_list)
        print(f"[{udid}] 点击视频号搜索按钮坐标: ({new_x}, {new_y})")
        tap_point(udid, new_x, new_y)
        time.sleep(2)  # 等待新的点击操作完成

        # 点击搜索框确保获得焦点
        tap_point(udid, 500, 190)
        time.sleep(2)  # 增加等待时间，确保焦点已获得

        # 输入关键字搜索
        tap_point(udid, 500, 190)
        time.sleep(1)
        input_text(udid, "hair\ clippers")
        time.sleep(1)
        search_x, search_y = random.choice(search_list)
        print(f"[{udid}] 点击视频号搜索按钮坐标: ({search_x}, {search_y})")
        tap_point(udid, search_x, search_y)
        time.sleep(2)  # 等待搜索结果加载

        #搜索结果视频点击区域结果x值为125-950，y值为1425-1910
        video_list = [
            (125, 1425),
            (125, 1450),
            (125, 1475),
            (525, 1500),
            (125, 1525),
            (125, 1550),
            (625, 1575),
            (125, 1600),
            (199, 1625),
            (125, 1650),
            (762, 1675),
            (872, 1700),
            (150, 1725),
            (279, 1750),
        ]
        video_x, video_y = random.choice(video_list)
        print(f"[{udid}] 点击视频号搜索结果视频坐标: ({video_x}, {video_y})")
        tap_point(udid, video_x, video_y)
        time.sleep(2)  # 等待视频加载

        # 继续后续操作
        slide = 5
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
                    # 发送到API，设置超时时间为10秒
                    api_response = send_screenshot_to_api(base64_data, udid, api_url)
                    print(f"[{udid}] API返回: {api_response}")

                    # 基础等待时间
                    base_wait_time = 2

                    # 根据API返回结果中的isInterested值决定操作
                    if api_response and isinstance(api_response, dict) and api_response.get('isInterested') == True:
                        # 点击评论按钮
                        comment_list = [(970, 2085), (1000, 2085), (1030, 2085), (1060, 2085), (1090, 2085)]
                        comment_x, comment_y = random.choice(comment_list)
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
                                 '540', '1800', '540', '1000', '300'],  # 增加滑动时间
                                check=True, timeout=5
                            )
                            time.sleep(random.uniform(0.5, 3))

                        for _ in range(down_swipes):
                            subprocess.run(
                                ['adb', '-s', udid, 'shell', 'input', 'swipe',
                                 '540', '1000', '540', '1800', '300'],  # 增加滑动时间
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
                        ['adb', '-s', udid, 'shell', 'input', 'swipe', '540', '2000', '540', '1000', '300'],  # 增加滑动时间
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


def check_live_stream(udid):
    """
    检查当前页面是否包含直播内容
    """
    try:
        # 使用UIAutomator dump当前界面
        subprocess.run(
            ['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        time.sleep(0.5)

        # 将xml文件拉到本地
        subprocess.run(
            ['adb', '-s', udid, 'pull', '/data/local/tmp/ui.xml', f'temp_{udid}.xml'],
            check=True
        )

        # 读取xml文件内容
        import xml.etree.ElementTree as ET
        tree = ET.parse(f'temp_{udid}.xml')
        root = tree.getroot()

        # 需要跳过的关键词列表
        skip_keywords = ['直播', '正在直播', 'LIVE']

        for node in root.findall(".//node[@class='android.widget.TextView']"):
            text = node.get('text', '').strip()
            if any(keyword in text for keyword in skip_keywords):
                print(f"[{udid}] 检测到需要跳过的内容: {text}")
                return True

        return False

    except Exception as e:
        print(f"[{udid}] 检查直播内容时出错: {e}")
        return False
    finally:
        # 清理临时文件
        try:
            if os.path.exists(f'temp_{udid}.xml'):
                os.remove(f'temp_{udid}.xml')
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        except:
            pass


def check_and_close_douyin_popup(udid):
    """
    检查并关闭抖音弹窗提示
    """
    try:
        print(f"[{udid}] 检查抖音弹窗...")

        # 使用UIAutomator获取当前界面信息
        subprocess.run(['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
                       check=True)
        time.sleep(1)

        result = subprocess.run(['adb', '-s', udid, 'shell', 'cat', '/data/local/tmp/ui.xml'],
                                stdout=subprocess.PIPE, text=True)

        # 解析XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(result.stdout)

        # 更新提示的特征
        update_indicators = {
            '以后再说': ['暂不更新', '稍后更新', '取消更新'],
            '关闭': ['关闭', '取消'],
            '我知道了': ['我知道了', '知道了'],
            '稍后再说': ['稍后再说', '下次再说']
        }

        # 首先检查更新提示
        for main_text, related_texts in update_indicators.items():
            # 检查主要文本和相关文本
            for text in [main_text] + related_texts:
                nodes = root.findall(f".//node[@text='{text}']")
                if nodes:
                    node = nodes[0]
                    bounds = node.get('bounds')
                    if bounds:
                        # 解析bounds字符串，格式类似 "[x1,y1][x2,y2]"
                        import re
                        coords = re.findall(r'\[(\d+),(\d+)\]', bounds)
                        if len(coords) == 2:
                            x = (int(coords[0][0]) + int(coords[1][0])) // 2
                            y = (int(coords[0][1]) + int(coords[1][1])) // 2
                            print(f"[{udid}] 找到{text}按钮，坐标: ({x}, {y})")

                            # 点击按钮
                            tap_point(udid, x, y)
                            time.sleep(1)

                            # 再次检查是否还有弹窗（有时候可能有多层弹窗）
                            return check_and_close_douyin_popup(udid)

        # 检查是否有更新对话框的特征
        update_dialog_indicators = ['发现新版本', '版本更新', '新版本', '立即更新']
        if any(indicator in result.stdout for indicator in update_dialog_indicators):
            print(f"[{udid}] 检测到更新对话框")
            # 尝试查找"以后再说"按钮
            later_nodes = root.findall(".//node[@text='以后再说']")
            if later_nodes:
                node = later_nodes[0]
                bounds = node.get('bounds')
                if bounds:
                    coords = re.findall(r'\[(\d+),(\d+)\]', bounds)
                    if len(coords) == 2:
                        x = (int(coords[0][0]) + int(coords[1][0])) // 2
                        y = (int(coords[0][1]) + int(coords[1][1])) // 2
                        print(f"[{udid}] 找到'以后再说'按钮，坐标: ({x}, {y})")
                        tap_point(udid, x, y)
                        time.sleep(1)
                        return True

        print(f"[{udid}] 未检测到弹窗")
        return False

    except Exception as e:
        print(f"[{udid}] 检查抖音弹窗失败: {e}")
        return False
    finally:
        # 清理临时文件
        try:
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        except:
            pass


def perform_douyin_operations(udid):
    """
    执行抖音的操作流程
    """
    try:
        print(f"[{udid}] 开始执行抖音操作")

        # 强制停止抖音
        force_stop_app(udid, "com.ss.android.ugc.aweme")
        time.sleep(2)

        # 启动抖音
        open_app(udid, "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.splash.SplashActivity")
        time.sleep(10)  # 等待应用启动

        # 检查并处理可能的弹窗
        try:
            check_and_close_douyin_popup(udid)
        except Exception as e:
            print(f"[{udid}] 处理抖音弹窗时出错: {e}")
            # 继续执行，不要因为弹窗处理失败就中断整个流程

        # 获取设备信息（从缓存中）
        device_info = cache_device_info(udid)
        if not device_info:
            print(f"[{udid}] 无法获取设备信息，停止操作")
            return

        # 使用缓存的坐标，计算视频区域的中心点
        screen_width = device_info['screen_width']
        screen_height = device_info['screen_height']
        center_x = screen_width // 2
        center_y = (screen_height * 2) // 5  # 屏幕高度的40%位置
        swipe_coords = device_info['coordinates']['swipe_start'] + device_info['coordinates']['swipe_end']

        # 随机执行滑动次数
        slide_count = 3
        print(f"[{udid}] 计划执行{slide_count}次滑动")

        # 设置API地址
        api_url = "https://iris.iigood.com/iris/v1/agent/interest"

        for i in range(slide_count):
            if not check_device_connected(udid):
                print(f"[{udid}] 设备已断开连接，停止操作")
                return

            print(f"[{udid}] 第{i + 1}次滑动操作")

            try:
                # 首先检查是否是直播内容
                if check_live_stream(udid):
                    print(f"[{udid}] 跳过直播内容")
                    # 直接滑动到下一个视频
                    subprocess.run(
                        ['adb', '-s', udid, 'shell', 'input', 'swipe'] +
                        [str(x) for x in swipe_coords] + ['300'],
                        check=True, timeout=5
                    )
                    time.sleep(random.uniform(1, 2))
                    continue

                # 如果不是直播内容，继续正常的处理流程
                base64_data = get_screenshot_base64(udid)
                if base64_data:
                    api_response = send_screenshot_to_api(base64_data, udid, api_url)
                    print(f"[{udid}] API返回: {api_response}")

                    if api_response and isinstance(api_response, dict) and api_response.get('isInterested') == True:
                        print(f"[{udid}] 准备点赞，点击坐标: ({center_x}, {center_y})")
                        # 双击点赞
                        tap_point(udid, center_x, center_y)
                        time.sleep(0.01)
                        tap_point(udid, center_x, center_y)
                        print(f"[{udid}] 双击点赞完成，点赞坐标是：{center_x},{center_y}")
                        time.sleep(0.5)

                        # 处理评论
                        comments = get_comments_ui(udid)
                        if comments:
                            process_comments(udid, comments, device_info)

                        # 随机等待
                        wait_time = random.randint(3, 10)
                        time.sleep(wait_time)

                # 滑动到下一个视频
                subprocess.run(
                    ['adb', '-s', udid, 'shell', 'input', 'swipe'] +
                    [str(x) for x in swipe_coords] + ['300'],
                    check=True, timeout=5
                )
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"[{udid}] 操作发生错误: {e}")
                continue

        print(f"[{udid}] 抖音操作完成")
        return
    except Exception as e:
        print(f"[{udid}] 抖音操作失败: {e}")
        return


def check_device_ready(udid):
    """
    检查设备是否准备就绪
    """
    try:
        # 检查设备是否响应
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'getprop', 'sys.boot_completed'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        if result.stdout.strip() != '1':
            print(f"[{udid}] 设备未完全启动")
            return False

        print(f"[{udid}] 设备已启动并响应")

        # 检查屏幕状态
        screen_state = is_screen_on(udid)
        print(f"[{udid}] 屏幕状态: {'亮起' if screen_state else '关闭'}")

        if not screen_state:
            print(f"[{udid}] 尝试唤醒屏幕...")
            # 尝试唤醒屏幕
            subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
            time.sleep(2)

            if not is_screen_on(udid):
                print(f"[{udid}] 尝试使用电源键唤醒...")
                subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', '26'])
                time.sleep(2)

        # 无论如何都尝解锁屏幕
        unlock_screen(udid)
        print(f"[{udid}] 设备检查完成，准备绪")
        return True

    except Exception as e:
        print(f"[{udid}] 设备检查失败: {e}")
        return False


def multi_platform_operations(udid):
    """
    执行多平台操作的主函数
    """
    if udid in completed_devices:
        print(f"[{udid}] 已执行过，跳过")
        return

    try:
        print(f"[{udid}] 开始执行多平台操作")
        #执行操作
        completed_devices.append(udid) #标记完成
        

        # 检查设备状态
        if not check_device_ready(udid):
            print(f"[{udid}] 设备未就绪，跳过操作")
            return

        # 确保屏幕解锁
        ensure_screen_unlocked(udid)

        # 1. 执行微信操作
        perform_operations(udid)  # 使用原有的微信操作函数

        # 2. 回到桌面
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
        time.sleep(2)

        # # 3. 执行抖音操作
        # perform_douyin_operations(udid)

        # # 4. 回到桌面
        # subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
        # time.sleep(2)

        # 5. 锁屏
        lock_screen(udid)

        print(f"[{udid}] 所有平台操作完成")
    except Exception as e:
        print(f"[{udid}] 多平台操作时发生错误: {e}")


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


def process_comments(udid, comments, device_info):
    """
    改进的评论处理功能
    """
    try:
        # 过滤评论
        filtered_comments = []
        for comment in comments:
            # 移除特殊字符和表情
            cleaned_comment = re.sub(r'[^\w\s]', '', comment)
            # 检查长度和内容质量
            if len(cleaned_comment) >= 8 and not any(keyword in cleaned_comment.lower()
                                                     for keyword in ['广告', '推广', 'ad', '软件']):
                filtered_comments.append(cleaned_comment)

        if not filtered_comments:
            print(f"[{udid}] 没有找到有效的评论")
            return

        print(f"[{udid}] 过滤后的评论内容:")
        for idx, comment in enumerate(filtered_comments, 1):
            print(f"{idx}. {comment}")

        # 发送评论到API
        comments_api_url = "https://iris.iigood.com/iris/v1/agent/comment"
        payload = {
            'profile': '喜欢美妆和美女',
            'comments': filtered_comments[:5],  # 只发送前5条评论
            'device_info': {
                'udid': udid,
                'timestamp': datetime.now().isoformat(),
                'performance': monitor_device_performance(udid)
            }
        }

        response = requests.post(comments_api_url, json=payload,
                                 headers={'Content-Type': 'application/json'},
                                 timeout=10)
        response.raise_for_status()

        print(f"[{udid}] 评论发送成功: {response.json()}")

    except Exception as e:
        print(f"[{udid}] 处理评论失败: {e}")
        # 记录错误日志
        logging.error(f"评论处理失败 - 设备: {udid}, 错误: {str(e)}", exc_info=True)


def monitor_device_performance(udid):
    """
    监控设备性能指标
    """
    try:
        # 获取CPU使用率
        cpu_cmd = "dumpsys cpuinfo | grep TOTAL"
        cpu_result = subprocess.run(['adb', '-s', udid, 'shell', cpu_cmd],
                                    stdout=subprocess.PIPE, text=True)
        cpu_usage = cpu_result.stdout.strip()

        # 获取内存使用情况
        mem_cmd = "dumpsys meminfo"
        mem_result = subprocess.run(['adb', '-s', udid, 'shell', mem_cmd],
                                    stdout=subprocess.PIPE, text=True)
        mem_usage = mem_result.stdout.strip()

        # 获取电池信息
        battery_cmd = "dumpsys battery"
        battery_result = subprocess.run(['adb', '-s', udid, 'shell', battery_cmd],
                                        stdout=subprocess.PIPE, text=True)
        battery_info = battery_result.stdout.strip()

        return {
            'cpu': cpu_usage,
            'memory': mem_usage,
            'battery': battery_info
        }
    except Exception as e:
        print(f"[{udid}] 获取性能数据失败: {e}")
        return None


def check_device_status(udid):
    """
    全面的设备状态检查
    """
    try:
        status = {
            'connected': False,
            'screen_on': False,
            'battery_level': 0,
            'wifi_connected': False,
            'performance': None
        }

        # 检查设备连接
        if check_device_connected(udid):
            status['connected'] = True

            # 检查屏幕状态
            status['screen_on'] = is_screen_on(udid)

            # 检查电池电量
            battery_cmd = "dumpsys battery | grep level"
            battery_result = subprocess.run(['adb', '-s', udid, 'shell', battery_cmd],
                                            stdout=subprocess.PIPE, text=True)
            battery_level = int(battery_result.stdout.split(':')[1].strip())
            status['battery_level'] = battery_level

            # 检查WiFi连
            wifi_cmd = "dumpsys wifi | grep 'Wi-Fi is'"
            wifi_result = subprocess.run(['adb', '-s', udid, 'shell', wifi_cmd],
                                         stdout=subprocess.PIPE, text=True)
            status['wifi_connected'] = 'enabled' in wifi_result.stdout.lower()

            # 获取性能数据
            status['performance'] = monitor_device_performance(udid)

        return status
    except Exception as e:
        print(f"[{udid}] 检查设备状态失败: {e}")
        return None


def smart_wait(udid, condition_func, timeout=30, check_interval=1):
    """
    智能等待某个条件满足
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if condition_func(udid):
                return True
        except Exception as e:
            print(f"[{udid}] 等待条件检查失败: {e}")
        time.sleep(check_interval)
    return False


def wait_for_element(udid, text_or_resource_id, timeout=30):
    """
    等待特定元素出现
    """

    def check_element(udid):
        try:
            subprocess.run(['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
                           check=True)
            result = subprocess.run(['adb', '-s', udid, 'shell', 'cat', '/data/local/tmp/ui.xml'],
                                    stdout=subprocess.PIPE, text=True)
            return text_or_resource_id in result.stdout
        except:
            return False

    return smart_wait(udid, check_element, timeout)


def check_wechat_login(udid):
    """
    检查微信是否已登录，使用多个方法进行验证
    """
    try:
        print(f"[{udid}] 检查微信登录状态...")

        # 方法1: 检查是否存在登录界面的特征
        subprocess.run(['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
                       check=True)
        time.sleep(1)

        # 修改这里，添加encoding='utf-8'参数，并使用errors='ignore'来处理无法解码的字符
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'cat', '/data/local/tmp/ui.xml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',  # 指定使用UTF-8编码
            errors='ignore'    # 忽略无法解码的字符
        )

        # 清理临时文件
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])

        # 未登录状态的特征
        login_indicators = [
            '登录', '微信号/QQ号/邮箱', '手机号登录', '请填写手机号', '密码',
            '用微信号/QQ号/邮箱登录', '请输入密码', '同意并继续', '请先登录'
        ]

        # 已登录状态的特征
        logged_in_indicators = [
            '发现', '通讯录', '我', '朋友圈', '视频号', '扫一扫'
        ]

        # 检查是否存在未登录特征
        if any(indicator in result.stdout for indicator in login_indicators):
            print(f"[{udid}] 检测到登录界面，微信未登录")
            return False

        # 检查是否存在已登录特征
        if any(indicator in result.stdout for indicator in logged_in_indicators):
            print(f"[{udid}] 检测到主界面特征，微信已登录")
            return True

        # 方法2: 检查微信数据目录
        data_check = subprocess.run(
            ['adb', '-s', udid, 'shell', 'ls', '/data/data/com.tencent.mm/MicroMsg'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if 'wxacache' in data_check.stdout and 'CheckLoginHistory' in data_check.stdout:
            print(f"[{udid}] 检测到微信数据目录，微信可能已登录")
            return True

        # 方法3: 尝试点击"我"的位置
        tap_point(udid, 686, 2187)  # "我"的坐标
        time.sleep(1)

        # 再次检查界面
        subprocess.run(['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
                       check=True)
        result = subprocess.run(['adb', '-s', udid, 'shell', 'cat', '/data/local/tmp/ui.xml'],
                                stdout=subprocess.PIPE, text=True)
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])

        # 检查是否进入了个人页面
        profile_indicators = ['个人信息', '支付', '收藏', '设置']
        if any(indicator in result.stdout for indicator in profile_indicators):
            print(f"[{udid}] 成功进入个人页面，微信已登录")
            # 返回主页
            subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_BACK'])
            return True

        print(f"[{udid}] 无法确定登录状态，默认为未登录")
        return False

    except Exception as e:
        print(f"[{udid}] 检查微信登录状态失败: {e}")
        logging.error(f"检查微信登录状态失败 - 设备: {udid}, 错误: {str(e)}", exc_info=True)
        return False
    finally:
        # 确保清理临时文件
        try:
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        except:
            pass


def handle_wechat_login(udid):
    """
    处理微信登录流程
    """
    try:
        print(f"[{udid}] 开始处理微信登录...")

        # 等待登录界面加载
        if not wait_for_element(udid, "登录", timeout=10):
            print(f"[{udid}] 未检测到登录界面")
            return False

        # 这里可以添加自动登录的逻辑
        # 比如:
        # 1. 扫码登录
        # 2. 账号密码登录
        # 3. 手机号登录
        # 具体实现取决于登录方式的选择

        print(f"[{udid}] 请手动完成登录操作")

        # 等待登录完成
        for _ in range(30):  # 最多等待30秒
            if check_wechat_login(udid):
                print(f"[{udid}] 登录成功")
                return True
            time.sleep(1)

        print(f"[{udid}] 登录超时")
        return False

    except Exception as e:
        print(f"[{udid}] 处理微信登录失败: {e}")
        return False


def check_and_close_popup(udid, keyword):
    """
    微信视频号页面检查并关闭包含特定关键字的弹窗
    """
    try:
        # 使用UIAutomator获取当前界面信息
        subprocess.run(['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
                       check=True)
        time.sleep(2)

        result = subprocess.run(['adb', '-s', udid, 'shell', 'cat', '/data/local/tmp/ui.xml'],
                                stdout=subprocess.PIPE, text=True)

        # 解析XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(result.stdout)

        # 查找包含关键字的节点
        for node in root.findall(".//node[@text]"):
            text = node.get('text', '').strip()
            if keyword in text:
                bounds = node.get('bounds')
                if bounds:
                    # 解析bounds字符串，格式类似 "[x1,y1][x2,y2]"
                    import re
                    coords = re.findall(r'\[(\d+),(\d+)\]', bounds)
                    if len(coords) == 2:
                        x = (int(coords[0][0]) + int(coords[1][0])) // 2
                        y = (int(coords[0][1]) + int(coords[1][1])) // 2
                        print(f"[{udid}] 找到'{keyword}'按钮，坐标: ({x}, {y})")

                        # 点击按钮
                        tap_point(udid, x, y)
                        time.sleep(1)
                        return True

        print(f"[{udid}] 未检测到'{keyword}'关键字")
        return False

    except Exception as e:
        print(f"[{udid}] 检查弹窗失败: {e}")
        return False
    finally:
        # 清理临时文件
        try:
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        except:
            pass


def input_text(udid, text):
    """
    使用直接的adb shell input text命令输入文本
    """
    try:
        print(f"[{udid}] 准备输入文本: {text}")
        
        # 点击搜索框确保焦点
        tap_point(udid, 500, 190)
        time.sleep(1)
        
        # 清除现有文本
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_CLEAR'])
        time.sleep(1)
        
        # 直接使用完整的命令字符串
        cmd = f'adb -s {udid} shell input text "{text}"'
        subprocess.run(cmd, shell=True)
        
        print(f"[{udid}] 文本输入完成")
        return True
        
    except Exception as e:
        print(f"[{udid}] 输入文本失败: {e}")
        return False


if __name__ == "__main__":
    devices = get_connected_devices()
    if not devices:
        print("没有检测到连接的设备")
    else:
        print(f"检测到的设备: {devices}")

        # 多线程执行操作
        threads = []
        for udid in devices:
            thread = threading.Thread(target=multi_platform_operations, args=(udid,))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        print("所有设备的多平台操作完成")