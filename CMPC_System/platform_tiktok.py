#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/12/24 11:18
# @Author : Genesis Ai
# @File : platform_tiktok.py

import time
import logging
import sys
import random
import threading  # 添加到文件开头的导入部分
import base64
from datetime import datetime
import os
import requests
import sys
import re
import subprocess
import pytesseract
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")


def input_text(udid, text):
    """使用直接的adb shell input text 命令输入文本"""
    try:
        print(f"[{udid}] 输入文本: {text}")
        input_box_x = random.randint(330, 330)
        input_box_y = random.randint(189, 235)
        tap_point(udid, input_box_x, input_box_y)
        time.sleep(0.5)
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


def get_connected_devices():
    """获取已连接的设备列表"""
    try:
        result = subprocess.run(
            ['adb', 'devices'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        print("adb devices 输出:", result.stdout)
        print("错误输出:", result.stderr)

        devices = []
        unauthorized_devices = []

        for line in result.stdout.strip().split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    device_id = parts[0]
                    status = parts[1]
                    if status == 'device':
                        devices.append(device_id)
                    elif status == 'unauthorized':
                        unauthorized_devices.append(device_id)

        if unauthorized_devices:
            print("\n检测到未授权的设备:")
            for device in unauthorized_devices:
                print(f"设备 {device} 未授权，请在设备上允许 USB 调试:")
                print("1. 请在手机上查看是否有 USB 调试授权提示")
                print("2. 点击「允许 USB 调试」")
                print("3. 可以勾选「总是允许使用这台计算机进行调试」")
                print("4. 如果没有看到提示，请尝试：")
                print("   - 断开并重新连接 USB 线")
                print("   - 在设备上关闭再打开 USB 调试")
                print("   - 检查 USB 连接模式是否正确\n")

        print(f"已授权的设备: {devices}")
        return devices
    except Exception as e:
        print(f"获取设备列表时出错: {e}")
        return []


def is_screen_on(udid):
    """检查屏幕是否亮起"""
    try:
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'dumpsys', 'display | grep "mScreenState"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        print(f"[{udid}] 屏幕状态检查结果: {result.stdout}")
        return "ON" in result.stdout or "SCREEN_STATE_ON" in result.stdout
    except Exception as e:
        print(f"[{udid}] 检查屏幕状态时出错: {e}")
        return True


def unlock_screen(udid):
    """解锁设备屏幕（适用于无密码锁屏）"""
    print(f"[{udid}] 正在解锁屏幕")
    subprocess.run(['adb', '-s', udid, 'shell', 'input', 'swipe', '540', '2000', '540', '800'])
    time.sleep(2)
    if is_screen_on(udid):
        print(f"[{udid}] 屏幕已解锁")
    else:
        print(f"[{udid}] 无法解锁屏幕")


def ensure_screen_unlocked(udid):
    """确保屏幕被唤醒并解锁"""
    if not is_screen_on(udid):
        print(f"[{udid}] 屏幕关闭，正在唤醒")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
        time.sleep(1)
    unlock_screen(udid)


def get_screen_size(udid):
    """获取设备的屏幕分辨率"""
    ensure_screen_unlocked(udid)
    result = subprocess.run(['adb', '-s', udid, 'shell', 'wm', 'size'], stdout=subprocess.PIPE, text=True)
    size_lines = result.stdout.strip().split('\n')

    for line in size_lines:
        if "Physical size" in line:
            size = line.split(":")[1].strip()
            width, height = map(int, size.split("x"))
            print(f"[{udid}] 屏幕尺寸: {width}x{height}")
            return width, height

    try:
        size = size_lines[0].strip()
        width, height = map(int, size.split("x"))
        print(f"[{udid}] 屏幕尺寸: {width}x{height}")
        return width, height
    except Exception as e:
        print(f"[{udid}] 无法获取屏幕尺寸: {e}")
        return None, None


def check_device_status(udid):
    """检查设备状态"""
    try:
        status = {
            'connected': False,
            'screen_on': False,
            'battery_level': 0,
            'wifi_connected': False
        }

        # 检查设备连接
        result = subprocess.run(['adb', '-s', udid, 'get-state'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        status['connected'] = 'device' in result.stdout

        if status['connected']:
            # 检查屏幕状态
            status['screen_on'] = is_screen_on(udid)

            # 检查电池电量
            battery_cmd = "dumpsys battery | grep level"
            battery_result = subprocess.run(['adb', '-s', udid, 'shell', battery_cmd],
                                            stdout=subprocess.PIPE, text=True)
            battery_level = int(battery_result.stdout.split(':')[1].strip())
            status['battery_level'] = battery_level

            # 检查WiFi连接
            wifi_cmd = "dumpsys wifi | grep 'Wi-Fi is'"
            wifi_result = subprocess.run(['adb', '-s', udid, 'shell', wifi_cmd],
                                         stdout=subprocess.PIPE, text=True)
            status['wifi_connected'] = 'enabled' in wifi_result.stdout.lower()

        return status
    except Exception as e:
        print(f"[{udid}] 检查设备状态失败: {e}")
        return None


def get_screenshot_base64(udid):
    """
    获取设备截图并转换为base64，不保存到本地
    """
    try:
        print(f"[{udid}] 开始执行截屏操作...")

        # 清理设备上可能存在的旧截图
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'], check=True)
        print(f"[{udid}] 已清理旧截图")

        # 生成带时间戳的文件名，确保唯一性
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        device_filename = f"/data/local/tmp/screen_{timestamp}.png"

        # 截取新图片并直接读取为base64
        print(f"[{udid}] 正在截取屏幕...")
        subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', device_filename], check=True)

        # 直接从设备读取文件内容并转换为base64
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'cat', device_filename],
            stdout=subprocess.PIPE,
            check=True
        )

        # 转换为base64
        base64_data = base64.b64encode(result.stdout).decode('utf-8')

        # 清理设备上的临时文件
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', device_filename], check=True)

        print(f"[{udid}] Base64长度: {len(base64_data)}")
        return base64_data

    except Exception as e:
        print(f"[{udid}] 截图失败: {e}")
        # 发生错误时也要尝试清理临时文件
        try:
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'])
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
            'profile': '喜欢美女和汽车',
            'content': '',
            'attachments': [base64_data]
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{udid}] API请求失败: {e}")
        return None


def get_comments_ui(udid):
    """使用UIAutomator获取评论区的评论内容"""
    try:
        print(f"[{udid}] 开始获取评论内容...")

        # 等待评论区加载
        time.sleep(2)

        # 使用UIAutomator dump当前界面
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

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

        comments = []
        # 更新查找逻辑，更精确地定位评论内容
        for node in root.findall(".//node[@class='android.widget.TextView']"):
            text = node.get('text', '').strip()
            # 更新过滤条件
            if (text and
                    not text.startswith(('回复', '查看翻译', '查看更多回复', '点赞', '分享')) and
                    not text in ['评论', '点赞', '分享', '回复'] and
                    not text.endswith('条回复') and
                    not text.endswith('月') and  # 过滤时间信息
                    len(text) > 1):  # 过滤掉单个字符
                comments.append(text)

        # 清理临时文件
        os.remove(f'comments_{udid}.xml')
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])

        print(f"[{udid}] 获取到 {len(comments)} 条评论")
        for i, comment in enumerate(comments, 1):
            print(f"{i}. {comment}")
        return comments

    except Exception as e:
        print(f"[{udid}] 获取评论失败: {e}")
        # 清理临时文件
        try:
            if os.path.exists(f'comments_{udid}.xml'):
                os.remove(f'comments_{udid}.xml')
            subprocess.run(['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'])
        except:
            pass
        return []


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


def human_swipe(udid, start_x, start_y, end_x, end_y, duration=300):
    """
    模拟人类的滑动操作
    参数:
    - udid: 设备ID
    - start_x, start_y: 起始坐标
    - end_x, end_y: 结束坐标
    - duration: 滑动持续时间(毫秒)
    """
    try:
        # 计算基础偏移量
        distance_x = end_x - start_x
        distance_y = end_y - start_y

        # 生成3-5个中间点，使轨迹更自然
        points_count = random.randint(3, 5)
        points = [(start_x, start_y)]

        for i in range(points_count):
            # 进度百分比
            progress = (i + 1) / (points_count + 1)

            # 基础位置
            base_x = start_x + distance_x * progress
            base_y = start_y + distance_y * progress

            # 添加随机偏移，越靠近中间偏移越大
            offset_factor = 1 - abs(0.5 - progress) * 2  # 在中间点达到最大
            offset_x = random.randint(-30, 30) * offset_factor

            # 垂直方向的偏移较小
            offset_y = random.randint(-10, 10) * offset_factor

            points.append((
                int(base_x + offset_x),
                int(base_y + offset_y)
            ))

        points.append((end_x, end_y))

        # 计算每段的持续时间
        segment_duration = duration // len(points)

        # 执行滑动
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            # 每段的实际持续时间添加随机变化
            actual_duration = segment_duration + random.randint(-50, 50)
            actual_duration = max(50, min(actual_duration, 500))  # 确保在合理范围内

            subprocess.run(
                ['adb', '-s', udid, 'shell', 'input', 'swipe',
                 str(x1), str(y1), str(x2), str(y2), str(actual_duration)],
                check=True, timeout=5
            )

            # 每段之间添加极短的随机停顿
            time.sleep(random.uniform(0.01, 0.03))

        return True

    except Exception as e:
        print(f"[{udid}] 人工滑动模拟失败: {e}")
        return False


def mock_api_response():
    """模拟API响应，随机返回True或False"""
    is_interested = random.choice([True, False])
    return {
        'isInsterested': is_interested,
        'message': 'Mock API response',
        'timestamp': datetime.now().isoformat()
    }


def capture_screenshot_from_phone(udid, screenshot_path="/sdcard/screenshot.png", local_path="screenshot.png"):
    """
    在手机上截图并拉取到本地
    :param udid: 设备的唯一识别码
    :param screenshot_path: 手机端保存截图的路径
    :param local_path: 本地保存截图的路径
    """
    try:
        # 清理手机上的旧截图（如果存在）
        print(f"[{udid}] 清理旧截图...")
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', screenshot_path],
                       stderr=subprocess.DEVNULL)  # 忽略错误输出

        # 截图并保存到手机路径
        print(f"[{udid}] 截图中...")
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'screencap', '-p', screenshot_path],
            check=True,
            stderr=subprocess.PIPE,
            text=True
        )

        # 检查截图是否成功
        check_result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'ls', screenshot_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if check_result.returncode != 0:
            print(f"[{udid}] 截图未成功保存到设备")
            return None

        # 从手机拉取截图到本地
        print(f"[{udid}] 拉取截图到本地...")
        subprocess.run(['adb', '-s', udid, 'pull', screenshot_path, local_path], check=True)

        print(f"[{udid}] 截图已保存到本地：{local_path}")
        return local_path

    except subprocess.CalledProcessError as e:
        print(f"[{udid}] 截图失败: {e}")
        return None


def convert_image_to_base64(image_path):
    """
    将图片转换为 Base64 格式
    :param image_path: 图片文件的路径
    :return: Base64 字符串
    """
    try:
        with open(image_path, "rb") as image_file:
            base64_data = base64.b64encode(image_file.read()).decode('utf-8')
        print(f"图片已成功转换为 Base64")
        return base64_data
    except Exception as e:
        print(f"图片转换为 Base64 失败: {e}")
        return None


def decode_base64_to_image(base64_data):
    """
    将 Base64 数据解码为 OpenCV 图像对象
    :param base64_data: Base64 编码的图片数据
    :return: OpenCV 图像对象
    """
    try:
        # 将 Base64 转换为字节数据
        image_data = base64.b64decode(base64_data)
        # 使用 PIL 打开字节数据
        pil_image = Image.open(BytesIO(image_data))
        # 转换为 OpenCV 格式（numpy 数组）
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return open_cv_image
    except Exception as e:
        print(f"Base64 转换为图片失败: {e}")
        return None


def preprocess_image_from_base64(base64_data):
    """
    从 Base64 数据进行预处理：裁剪评论区、灰度化、放大、二值化
    """
    img = decode_base64_to_image(base64_data)
    if img is None:
        print("无法从 Base64 数据解码图像")
        return None

    # 裁剪仅保留评论区
    height, width, _ = img.shape
    # 假设评论区在屏幕的下半部分
    cropped_img = img[int(height * 0.5):height, 0:width]

    # 放大图片
    scale_percent = 200  # 放大 200%
    width = int(cropped_img.shape[1] * scale_percent / 100)
    height = int(cropped_img.shape[0] * scale_percent / 100)
    dim = (width, height)
    cropped_img = cv2.resize(cropped_img, dim, interpolation=cv2.INTER_CUBIC)

    # 转为灰度图
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 保存处理后的图像用于调试
    cv2.imwrite("processed_image_debug.png", binary)
    return binary


def extract_comments_from_base64(base64_data):
    """
    从 Base64 数据中提取评论信息
    """
    # 1. 图像预处理
    processed_img = preprocess_image_from_base64(base64_data)
    if processed_img is None:
        print("图像预处理失败")
        return []

    # 2. OCR 提取文本
    extracted_text = pytesseract.image_to_string(processed_img, lang='eng+chi_sim')
    print("提取的原始文本内容：")
    print(extracted_text)

    # 3. 清理文本内容
    cleaned_text = clean_text(extracted_text)
    print("清理后的文本内容：")
    print(cleaned_text)

    # 4. 解析评论
    comments = parse_comments(cleaned_text)
    if not comments:
        print(f"[未能获取到评论]，清理后的文本内容：")
        print(cleaned_text)
        return []

    print("解析的评论信息：")
    for idx, comment in enumerate(comments, start=1):
        print(f"{idx}. 用户名: {comment['username']}, 评论: {comment['comment']}")
    return comments


def get_comments_from_screenshot(udid):
    """使用截图方式获取评论内容"""
    try:
        print(f"[{udid}] 开始通过截图获取评论内容...")

        # 等待评论区加载
        time.sleep(2)

        # 确保目标目录存在
        save_dir = r"E:\代码截图temp"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"[{udid}] 创建保存目录: {save_dir}")

        # 生成唯一的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        local_filename = f"comments_{udid}_{timestamp}.png"
        local_path = os.path.join(save_dir, local_filename)
        device_path = f"/sdcard/comments_{udid}.png"

        # 直接使用adb命令截图
        print(f"[{udid}] 开始截取评论区...")
        subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', device_path], check=True)

        # 将截图从设备拷贝到本地
        print(f"[{udid}] 正在保存截图到本地: {local_path}")
        subprocess.run(['adb', '-s', udid, 'pull', device_path, local_path], check=True)

        if not os.path.exists(local_path):
            print(f"[{udid}] 截图保存失败")
            return []

        print(f"[{udid}] 截图已成功保存到: {local_path}")

        # 将截图转换为Base64
        base64_data = convert_image_to_base64(local_path)
        if not base64_data:
            print(f"[{udid}] 图片转换失败")
            return []

        # 预处理图像并提取评论
        processed_img = preprocess_image_from_base64(base64_data)
        if processed_img is None:
            print(f"[{udid}] 图像预处理失败")
            return []

        # 使用OCR提取评论
        comments = extract_comments_from_base64(base64_data)

        # 清理设备上的临时文件
        subprocess.run(['adb', '-s', udid, 'shell', f'rm {device_path}'])

        if comments:
            print(f"[{udid}] 成功获取 {len(comments)} 条评论:")
            for i, comment in enumerate(comments, 1):
                print(f"{i}. {comment}")
            return comments
        else:
            print(f"[{udid}] 未能获取到评论")
            return []

    except Exception as e:
        print(f"[{udid}] 获取评论失败: {e}")
        return []


def open_instagram(udid):
    """打开 Instagram 应用，进行Instagram的一系列操作"""
    try:
        print(f"[{udid}] 正在打开 Instagram...")

        # # 先强制停止 Instagram 应用
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'am', 'force-stop', 'com.instagram.android'
        ])
        time.sleep(2)

        # 启动 Instagram 主界面
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'am', 'start', '-n',
            'com.instagram.android/com.instagram.mainactivity.InstagramMainActivity'
        ])
        time.sleep(4)  # 等待应用启动
        print(f"[{udid}] Instagram 已启动")

        # 首页搜索按钮图标坐标
        search_id_x = random.randint(295, 372)
        search_id_y = random.randint(2045, 2103)

        # 确认搜索按钮坐标
        confirm_id_x = random.randint(930, 1010)
        confirm_id_y = random.randint(2020, 2090)

        # 针对搜索结果页面进行处理
        up_swipes = random.randint(1, 3)
        down_swipes = random.randint(1, 3)

        print(f"点击搜索按钮：（{search_id_x},{search_id_y}）")
        tap_point(udid, search_id_x, search_id_y)
        time.sleep(1)
        input_text(udid, text="Young\ Woman")  # 输入搜索文本
        tap_point(udid, confirm_id_x, confirm_id_y)
        time.sleep(5)

        # 切换视频板块Reels
        reels_id_x = random.randint(980, 1027)
        reels_id_y = random.randint(350, 360)
        print(f"[{udid}]点击Reels按钮：（{reels_id_x},{reels_id_y}）")
        tap_point(udid, reels_id_x, reels_id_y)
        time.sleep(3)

        print(f"[{udid}] 结果页面模拟滑动: 向上{up_swipes}次, 向下{down_swipes}次")

        # 在搜索结果页面滑动
        for _ in range(up_swipes):
            # 生成随机的起点和终点坐标，保持在域内
            start_x = random.randint(301, 840)  # 在中心区域随机
            end_x = random.randint(120, 970)
            start_y = 1732  # 下部区域
            end_y = 800  # 上部区域

            # 使用人工滑动
            human_swipe(udid, start_x, start_y, end_x, end_y,
                        # 滑动时间随机，模拟人类真实行为
                        duration=random.randint(250, 350))
            time.sleep(random.uniform(1, 3))

        for _ in range(down_swipes):
            # 生成随机的起点和终点坐标，保持在区域内
            start_x = random.randint(120, 970)
            end_x = random.randint(120, 970)
            start_y = 1000  # 上部区域
            end_y = 1800  # 下部区域

            # 使用人工滑动
            human_swipe(udid, start_x, start_y, end_x, end_y,
                        duration=random.randint(250, 350))
            time.sleep(random.uniform(0.5, 2))

        # 随机等待一下，模拟人工浏览
        time.sleep(random.uniform(0.5, 1.5))

        # 在限定区域内随机选择一个点击位置
        random_click_x = random.randint(130, 950)
        random_click_y = random.randint(610, 1880)

        print(f"[{udid}] 在搜索结果页面随机点击位置: ({random_click_x}, {random_click_y})")
        tap_point(udid, random_click_x, random_click_y)
        time.sleep(2)  # 等待内容加载

        # 继续执行后续的视频滑动操作...
        slide = 4
        api_url = "https://iris.iigood.com/iris/v1/agent/interest"

        # 开始循环滑动视频
        for i in range(slide):
            # 每次检查设备是否还连接，如果断开，则重新连接
            if not check_device_status(udid):
                try:
                    print(f"[{udid}] 设备断开，重新连接")
                    subprocess.run(['adb', '-s', udid, 'connect'])
                    time.sleep(1)
                except Exception as e:
                    print(f"[{udid}] 设备断开，重新连接失败: {e}")
                    return

            print(f"进行第{i + 1}次滑动")
            try:
                # 获取截图转换为Base64
                base64_data = get_screenshot_base64(udid)
                if not base64_data:
                    print(f"[{udid}] 获取截图失败")
                    continue

                # 获取API响应
                api_response = mock_api_response()
                print(f"[{udid}] 模拟 API 响应: {api_response}")

                # 设定基础等待时间
                base_wait_time = random.randint(2, 7)

                # 根据API返回结果判断是否感兴趣
                if api_response and isinstance(api_response, dict) and api_response.get('isInsterested') == True:
                    # 先等待基础时间
                    time.sleep(base_wait_time)

                    # 点击评论区
                    comment_id_x = random.randint(950, 1015)
                    comment_id_y = random.randint(1365, 1450)
                    tap_point(udid, comment_id_x, comment_id_y)
                    print(f"[{udid}] 评论区已打开")
                    time.sleep(2)  # 内容加载

                    # 评论区滑动
                    up_swipes = random.randint(2, 5)
                    down_swipes = random.randint(1, 5)
                    print(f"[{udid}] 上下滑动次数: {up_swipes}次, {down_swipes}次")

                    # 在评论区滑动
                    for _ in range(up_swipes):
                        # 生成随机的起点和终点坐标，保持在评论区域内
                        start_x = random.randint(520, 560)  # 在中心区域随机
                        end_x = random.randint(520, 560)
                        start_y = 1800  # 下部区域
                        end_y = 1000  # 上部区域

                        # 使用人工滑动
                        human_swipe(udid, start_x, start_y, end_x, end_y,
                                    duration=random.randint(250, 350))
                        time.sleep(random.uniform(0.5, 2))

                    for _ in range(down_swipes):
                        # 生成随机的起点和终点坐标，保持在评论区域内
                        start_x = random.randint(520, 560)
                        end_x = random.randint(520, 560)
                        start_y = 1000  # 上部区域
                        end_y = 1800  # 下部区域

                        # 使用人工滑动
                        human_swipe(udid, start_x, start_y, end_x, end_y,
                                    duration=random.randint(250, 350))
                        time.sleep(random.uniform(0.5, 2))

                    # 获取评论信息
                    comments = get_comments_from_screenshot(udid)
                    if comments:
                        print(f"[{udid}] 获取到{len(comments)}条评论")
                        for idx, comment in enumerate(comments, 1):
                            print(f"{idx}.{comment}")
                        # 发送评论到API
                        comments_api_url = "https://iris.iigood.com/iris/v1/agent/comment"
                        comments_response = send_comments_to_api(comments, udid, comments_api_url)
                        if comments_response:
                            print(f"[{udid}] 评论API返回: {comments_response}")

                    # 关闭评论区
                    print(f"[{udid}] 关闭评论区")
                    comment_id_x = random.randint(340, 650)
                    comment_id_y = random.randint(370, 540)
                    tap_point(udid, comment_id_x, comment_id_y)
                    time.sleep(1)
                    # 双击屏幕点赞
                    randomclick_number = random.randint(1, 9)
                    print(f"[{udid}] 随机生成的数是: {randomclick_number}")
                    if randomclick_number % 2 == 0:
                        print(f"[{udid}] 随机数为偶数，执行双击点赞操作")
                        tap_point(udid, 500, 1500)
                        time.sleep(0.1)
                        tap_point(udid, 500, 1500)
                    else:
                        print(f"[{udid}] 随机数为奇数，跳过双击点赞操作")
                    # 随机选择是否点关注
                    random_number = random.randint(1, 9)
                    print(f"[{udid}] 随机生成的数是: {random_number}")
                    if random_number % 2 == 0:
                        print(f"[{udid}] 随机数为偶数，执行点击关注操作")
                        click_keyword(udid, base64_data, "关注")
                    else:
                        print(f"[{udid}] 随机数为奇数，跳过关注操作")

                    # 计算并执行总等待时间
                    extra_wait_time = random.randint(1, 60)
                    total_wait_time = base_wait_time + extra_wait_time
                    print(f"[{udid}] 总等待时间: {total_wait_time}秒")
                    time.sleep(total_wait_time)
                else:
                    print(f"[{udid}] isInterested为False,等待{base_wait_time}秒")
                    time.sleep(base_wait_time)
                    swipe_to_next_video(udid)

                    # 如果不是最后一次循环，执行滑动
                    if i < slide - 1:
                        print(f"[{udid}] 滑动到下一个视频")
                        start_next_x = random.randint(460, 1000)
                        end_next_x = random.randint(540, 840)
                        start_next_y = 1650
                        end_next_y = 540

                        human_swipe(udid, start_next_x, start_next_y, end_next_x, end_next_y,
                                    duration=random.randint(250, 350))
                        time.sleep(random.uniform(0.5, 2))

            except Exception as e:
                print(f"[{udid}] 操作发生错误: {e}")
                return False

        print(f"[{udid}] 所有滑动操作完成")
        # 关闭应用
        close_instagram(udid)
        return True

    except Exception as e:
        print(f"[{udid}] Instagram 操作失败: {e}")
        try:
            close_instagram(udid)
        except Exception as close_error:
            print(f"[{udid}] 关闭应用失败: {close_error}")
        return False


def swipe_to_next_video(udid):
    print(f"[{udid}] 开始滑动到下一个视频...")
    # 打印滑动开始时间
    print(f"[{udid}] 滑动时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    start_x = 500
    start_y = 1500
    end_x = 500
    end_y = 500

    human_swipe(udid, start_x, start_y, end_x, end_y, duration=500)
    time.sleep(2)

    print(f"[{udid}] 滑动完成")


def find_keyword_coordinates(image_path, keyword="关注"):
    """
    从图片中查找指定关键字的位置，并返回其坐标(关注)
    """
    # 加载图像
    img = cv2.imread(image_path)

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用 pytesseract 提取文字和位置信息
    data = pytesseract.image_to_data(gray, lang='chi_sim', output_type=pytesseract.Output.DICT)

    # 遍历所有文字，寻找关键字
    for i, text in enumerate(data["text"]):
        if keyword in text:  # 如果找到关键字
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            # 计算中心坐标
            center_x, center_y = x + w // 2, y + h // 2
            print(f"找到关键字 '{keyword}'，中心坐标: ({center_x}, {center_y})")
            return center_x, center_y

    print(f"未找到关键字 '{keyword}'")
    return None


def click_keyword(udid, image_path, keyword="关注"):
    """
    查找并点击页面上的关键字
    """
    coordinates = find_keyword_coordinates(image_path, keyword)
    if coordinates:
        center_x, center_y = coordinates
        print(f"[{udid}] 点击关键字 '{keyword}' 的坐标: ({center_x}, {center_y})")
        tap_point(udid, center_x, center_y)
    else:
        print(f"[{udid}] 未找到关键字 '{keyword}'，无法点击")


def back_to_home(udid):
    """返回手机桌面"""
    try:
        print(f"[{udid}] 正在返回桌面...")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
        time.sleep(1)
        print(f"[{udid}] 已返回桌面")
        return True
    except Exception as e:
        print(f"[{udid}] 返回桌面失败: {e}")
        return False


def tap_point(udid, x, y):
    """点击指定坐标"""
    try:
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'tap', str(x), str(y)])
        time.sleep(0.5)  # 等待点击响应
        return True
    except Exception as e:
        print(f"[{udid}] 点击失败: {e}")
        return False


def close_instagram(udid):
    """关闭 Instagram 应用并返回桌面"""
    try:
        print(f"[{udid}] 正在关闭 Instagram...")
        # 强制停止 Instagram 应用
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'am', 'force-stop', 'com.instagram.android'
        ], check=True)
        time.sleep(1)

        # 返回桌面
        back_to_home(udid)
        print(f"[{udid}] Instagram 已关闭并返回桌面")
        return True
    except Exception as e:
        print(f"[{udid}] 关闭 Instagram 失败: {e}")
        return False


def process_device(udid):
    """处理单个设备的所有操作流程"""
    import pytesseract
    # 显式设置路径
    pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\tesseract.exe"
    try:
        print(f"\n开始处理设备 {udid}")
        status = check_device_status(udid)
        if status:
            print(f"设备 {udid} 状态:")
            print(f"- 连接状态: {'已连接' if status['connected'] else '未连接'}")
            print(f"- 屏幕状态: {'已亮起' if status['screen_on'] else '已关闭'}")
            print(f"- 电池电量: {status['battery_level']}%")
            print(f"- WiFi状态: {'已连接' if status['wifi_connected'] else '未连接'}")

            if not status['screen_on']:
                ensure_screen_unlocked(udid)

            # 先返回桌面
            back_to_home(udid)
            time.sleep(1)

            # 打开 Instagram 并执行操作
            open_instagram(udid)
    except Exception as e:
        print(f"[{udid}] 设备处理过程出错: {e}")


# 验证是否成功切换到 Reels（可选）
def check_reels_tab(udid):
    try:
        # 使用 UI Automator 检查当前页面
        subprocess.run(['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'])
        result = subprocess.run(['adb', '-s', udid, 'shell', 'cat', '/data/local/tmp/ui.xml'],
                                stdout=subprocess.PIPE, text=True)
        return 'Reels' in result.stdout
    except:
        return False


def parse_comments(text):
    """
    解析 OCR 提取的文本内容，识别用户名和评论
    """
    lines = text.split("\n")
    comments = []
    current_comment = None

    for line in lines:
        # 如果是用户名和时间标识的格式，开始新评论
        if re.match(r'^\w+[\w.]*\s\d+[周月日]*$', line):  # 匹配用户名和时间
            if current_comment:
                comments.append(current_comment)
            current_comment = {"username": line.split()[0], "comment": ""}
        elif current_comment:  # 将内容追加到当前评论
            current_comment["comment"] += " " + line.strip()

    # 添加最后一个评论
    if current_comment:
        comments.append(current_comment)

    return comments


def clean_text(text):
    """
    清理 OCR 提取的文本内容
    """
    # 删除无意义的特殊字符
    cleaned_text = re.sub(r'[^\w\s@.,!?-]', '', text)
    # 去掉过多的空行
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
    return cleaned_text.strip()


if __name__ == "__main__":
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\tesseract.exe"
    # 获取所有连接的设备
    devices = get_connected_devices()
    if not devices:
        print("没有检测到连接的设备")
    else:
        print(f"检测到 {len(devices)} 台设备，开始并行处理")

        # 创建线程列表
        threads = []

        # 为每个设备创建并启动一个单独线程
        for udid in devices:
            thread = threading.Thread(
                target=process_device,
                args=(udid,),
                name=f"Device-{udid}"
            )
            threads.append(thread)
            thread.start()
            print(f"已启动设备 {udid} 的处理线程")

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        print("\n所有设备处理完成")