#!/usr/bin/env python
import io
# -- coding: utf-8 --
# @Time : 2024/12/24 14:25
# @Author : Genesis Ai
# @File : platfrom_facebook.py

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
from PIL import Image, ImageEnhance
import numpy as np
from io import BytesIO

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s")
"""使用直接的adb shell input text 命令输入文本"""
def fb_input_text(udid, text):
    try:
        if text is None:
            raise ValueError("输入文本不能为空")
        
        print(f"[{udid}] 输入文本: {text}")
        # 输入框的坐标
        input_box_x = random.randint(281, 700)
        input_box_y = random.randint(178, 227)
        fb_tap_point(udid, input_box_x, input_box_y)
        time.sleep(0.5)
        # 清除现有文本
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_CLEAR'])
        time.sleep(1)
        # 处理特殊字符
        safe_text = text.replace(" ", "%s")
        # 直接使用完整的命令字符串
        cmd = f'adb -s {udid} shell input text "{safe_text}"'
        subprocess.run(cmd, shell=True)

        print(f"[{udid}] 文本输入完成")
        return True
    except Exception as e:
        print(f"[{udid}] 输入文本失败: {e}")
        return False

"""获取已连接的设备列表"""
def fb_get_connected_devices():
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

"""检查屏幕是否亮起"""
def fb_is_screen_on(udid):
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

"""解锁设备屏幕（适用于无密码锁屏）"""
def fb_unlock_screen(udid):
    print(f"[{udid}] 正在解锁屏幕")
    subprocess.run(['adb', '-s', udid, 'shell', 'input', 'swipe', '540', '2000', '540', '800'])
    time.sleep(2)
    if fb_is_screen_on(udid):
        print(f"[{udid}] 屏幕已解锁")
    else:
        print(f"[{udid}] 无法解锁屏幕")

"""确保屏幕被唤醒并解锁"""
def fb_ensure_screen_unlocked(udid):
    if not fb_is_screen_on(udid):
        print(f"[{udid}] 屏幕关闭，正在唤醒")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
        time.sleep(1)
    fb_unlock_screen(udid)

"""获取设备的屏幕分辨率"""
def fb_get_screen_size(udid):
    fb_ensure_screen_unlocked(udid)
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

"""检查设备状态"""
def fb_check_device_status(udid):
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
            status['screen_on'] = fb_is_screen_on(udid)

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


        # 清理设备上的临时文件
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', device_filename], check=True)

        return base64_data
    except Exception as e:
        print(f"[{udid}] 截图失败: {e}")
        return None

"""使用UIAutomator获取评论区的评论内容"""


"""
    模拟人类的滑动操作
    参数:
    - udid: 设备ID
    - start_x, start_y: 起始坐标
    - end_x, end_y: 结束坐标
    - duration: 滑动持续时间(毫秒)
"""
def fb_human_swipe(udid, start_x, start_y, end_x, end_y, duration=300):
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

"""模拟API响应，随机返回True或False"""
def fb_mock_api_response():
    #is_interested = random.choice([True, False])
    is_interested = True
    return {
        'isInsterested': is_interested,
        'message': 'Mock API response',
        'timestamp': datetime.now().isoformat()
    }

"""
    在手机上截图并拉取到本地
    :param udid: 设备的唯一识别码
    :param screenshot_path: 手机端保存截图的路径
    :param local_path: 本地保存截图的路径
    """
def fb_capture_screenshot_from_phone(udid, screenshot_path="/sdcard/screenshot.png", local_path="screenshot.png"):
    try:
        # 清理手机上的旧截图（如果存在）
        print(f"[{udid}] 清理截图...")
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

"""
    将图片转换为 Base64 格式
    :param image_path: 图片文件的路径
    :return: Base64 字符串
"""
def fb_convert_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_data = base64.b64encode(image_file.read()).decode('utf-8')
        print(f"图片已成功转换为 Base64")
        return base64_data
    except Exception as e:
        print(f"图片转换为 Base64 失败: {e}")
        return None

"""搜索结果页面截图并处理图像Reels"""
def fb_capture_and_process_image(udid):
    screenshot_path = fb_capture_screenshot_from_phone(udid)  # 保存截图到本地
    image = Image.open(screenshot_path)
    return image

"""从截图中识别 Reels 按钮的坐标"""
def fb_find_reels_button(image):
    try:
        # 转换为灰度图
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        # 使用 OCR 获取带位置数据的结果
        ocr_data = pytesseract.image_to_data(gray_image, lang="eng", output_type=pytesseract.Output.DICT)
        
        # 遍历识别到的文本
        for i, text in enumerate(ocr_data['text']):
            if "Reels" in text:  # 匹配 Reels 文本
                x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                print(f"识别到 Reels 按钮位置: ({x}, {y}, {w}, {h})")
                # 返回按钮的中心点
                return x + w // 2, y + h // 2
        print("未找到 Reels 按钮")
        return None
    except Exception as e:
        print(f"OCR 识别失败: {e}")
        return None
    
"""自动识别并点击 Reels 按钮"""
def fb_tap_reels_button(udid):
    print(f"开始识别Reels按钮位置")
    # 获取截图
    image = fb_capture_and_process_image(udid)
    
    # 识别 Reels 按钮位置
    button_position = fb_find_reels_button(image)
    
    if button_position:
        # 点击 Reels 按钮
        x, y = button_position
        print(f"[{udid}] 点击 Reels 按钮：({x}, {y})")
        fb_tap_point(udid, x, y)
    else:
        print(f"[{udid}] 未找到 Reels 按钮，无法点击")    

"""将 Base64 数据解码为 OpenCV 图像"""
def fb_base64_to_image(base64_data):
    try:
        # 去掉前缀并解码 Base64 数据
        if "data:image" in base64_data:
            base64_data = base64_data.split(",")[1]

        image_data = base64.b64decode(base64_data)

        # 转换为 OpenCV 图像
        pil_image = Image.open(BytesIO(image_data))
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return open_cv_image
    except Exception as e:
        print(f"Base64 转图片失败: {e}")
        return None
"""滑动到下一个视频"""
swipe_lock = threading.Lock()
def fb_swipe_to_next_video(udid):
    start_x = 500
    start_y = 1500
    end_x = 500
    end_y = 500
    with swipe_lock:
        print(f"[{udid}]开始滑动到下一个视频******")
        fb_human_swipe(udid,start_x,start_y, end_x, end_y,duration=500)
        time.sleep(2)

"""从 Base64 数据预处理图片，包括裁剪评论区、灰度化、二值化"""
def fb_preprocess_image_from_base64(base64_data):
    try:
        img = fb_base64_to_image(base64_data)
        if img is None:
            print("无法从 Base64 数据解码图片")
            return None

        # 裁剪评论区域
        height, width, _ = img.shape
        cropped_img = img[int(height * 0.4):height, 0:width]  # 根据截图裁剪评论区

        # 转为灰度图
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

        # 自适应阈值二值化
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # 保存处理后的图片供调试（可选）
        cv2.imwrite("processed_comments_debug.png", binary)
        return binary
    except Exception as e:
        print(f"预处理 Base64 图片失败: {e}")
        return None

"""在视频页面进行截图分析是否包含（关键字信息）"""
def fb_capture_screenshot_as_base64(udid):
    """
    截图设备当前屏幕并返回 Base64 编码数据。
    :param udid: 设备的唯一标识符。
    :return: 图片的 Base64 字符串。
    """
    # 设备中临时截图路径
    temp_device_path = "/sdcard/temp_screenshot.png"
    # 执行 adb 命令进行截图
    subprocess.run(f"adb -s {udid} shell screencap -p {temp_device_path}", shell=True, check=True)
    # 从设备中读取截图到内存
    result = subprocess.run(
        f"adb -s {udid} exec-out cat {temp_device_path}",
        shell=True,
        stdout=subprocess.PIPE,
        check=True
    )
    # 将设备上的临时截图删除
    subprocess.run(f"adb -s {udid} shell rm {temp_device_path}", shell=True, check=True)
    # 通过 PIL 读取图片数据，确保格式正确
    image = Image.open(BytesIO(result.stdout))

    # 将图片转为 Base64 编码
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return base64_image

"""
判断 Base64 图片中是否包含目标文字。
:param base64_image: Base64 编码的图片
:param target_text: 要匹配的目标文字
:return: 如果包含目标文字，返回 True；否则返回 False
"""
def fb_contains_text(base64_image: str, target_text: str) -> bool:
    try:
        # 解码 Base64 图片为二进制数据
        image_data = base64.b64decode(base64_image)
        
        # 将二进制数据转换为图片对象
        image = Image.open(BytesIO(image_data))
        
        # 提取图片中的文字
        extracted_text = pytesseract.image_to_string(image, lang="chi_sim")
        
        # 清理文字（去掉空格和特殊字符）
        cleaned_text = re.sub(r'\s+', '', extracted_text)  # 去除所有空格
        cleaned_text = re.sub(r'[^\w\u4e00-\u9fff]', '', cleaned_text)  # 去除非中文和非字母数字字符
        
        # 检查是否包含目标文字
        return target_text in cleaned_text
    
    except Exception as e:
        print(f"处理图片时出错：{e}")
        return False


"""打开 Facebook 应用，进行Facebook的一系列操作"""
def fb_open_facebook(udid):
    try:
        print(f"[{udid}] 正在打开 Facebook...")

        # 先强制停止 Facebook 应用
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'am', 'force-stop', 'com.facebook.katana'
        ])
        time.sleep(2)

        # 修改启动方式，使用更通用的启动命令
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'monkey', '-p', 'com.facebook.katana', '-c', 'android.intent.category.LAUNCHER', '1'
        ])

        # 增加启动等待时间
        time.sleep(5)  # 给应用更多启动时间

        # 验证应用是否成功启动
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'dumpsys', 'window', 'windows'],
            stdout=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        # 使用 Python 过滤
        if 'mCurrentFocus' in output:
            print(output)

        # 过滤出com.facebook.katana
        if 'com.facebook.katana' in output:
            print(f"[{udid}] Facebook 已成功启动")
        else:
            print(f"[{udid}] Facebook 启动可能失败，尝试备用方法")

        print(f"[{udid}] Facebook 启动流程完成")

        # 首页搜索按钮图标坐标
        search_id_x = random.randint(845, 905)
        search_id_y = random.randint(190, 220)

        # 确认搜索按钮坐标
        confirm_id_x = random.randint(930, 1010)
        confirm_id_y = random.randint(2020, 2090)

        # 针对搜索结果页面进行处理
        up_swipes = random.randint(1, 3)
        down_swipes = random.randint(1, 3)

        print(f"点击搜索按钮：（{search_id_x},{search_id_y}）")
        fb_tap_point(udid, search_id_x, search_id_y)
        time.sleep(1)
        fb_input_text(udid, text="charming\ Girl")  # 输入搜索文本
        fb_tap_point(udid, confirm_id_x, confirm_id_y)#确认搜索
        time.sleep(5)

        # 切换视频板块Reels
        # reels_id_x = random.randint(900, 988)
        # reels_id_y = random.randint(310, 370)
        # print(f"[{udid}]点击Reels按钮：（{reels_id_x},{reels_id_y}）")
        # fb_tap_point(udid, reels_id_x, reels_id_y)
        # time.sleep(3)
        #切换视频板块Reels
        fb_tap_reels_button(udid)
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
            fb_human_swipe(udid, start_x, start_y, end_x, end_y,
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
            fb_human_swipe(udid, start_x, start_y, end_x, end_y,
                        duration=random.randint(250, 350))
            time.sleep(random.uniform(0.5, 2))

        # 随机等待一下，模拟人工浏览
        time.sleep(random.uniform(2, 3))

        # 在限定区域内随机选择一个点击位置
        random_click_x = random.randint(130, 950)
        random_click_y = random.randint(610, 1880)

        print(f"[{udid}] 在搜索结果页面随机点击位置: ({random_click_x}, {random_click_y})")
        fb_tap_point(udid, random_click_x, random_click_y)
        time.sleep(2)  # 等待内容加载
        # 继续执行后续的视频滑动操作...
        slide = 2
        api_url = "https://iris.iigood.com/iris/v1/agent/interest"

        # 开始循环滑动视频
        for i in range(slide):
            # 每次检查设备是否还连接，如果断开，则重新连接
            if not fb_check_device_status(udid):
                try:
                    print(f"[{udid}] 设备断开，重新连接")
                    subprocess.run(['adb', '-s', udid, 'connect'])
                    time.sleep(1)
                except Exception as e:
                    print(f"[{udid}] 设备断开，重新连接失败: {e}")
                    return

            print(f"进行第{i + 1}次滑动")
            fb_swipe_to_next_video(udid)
            try:
                # 获取API响应
                api_response = fb_mock_api_response()
                print(f"[{udid}] 模拟 API 响应: {api_response}")

                # 设定基础等待时间
                base_wait_time = random.randint(2, 7)

                # 根据API返回结果判断是否感兴趣
                if api_response and isinstance(api_response, dict) and api_response.get('isInsterested') == True:
                    # 先等待基础时间
                    time.sleep(base_wait_time)


                    # 判断是否包含“赞助内容”
                    base64_data_images = fb_capture_screenshot_as_base64(udid)
                    if fb_contains_text(base64_data_images, "赞助内容"):
                        print("图片中包含“赞助内容”四个字")
                        return True
                    else:
                        # 如果不包含“赞助内容”，则点击评论区
                        print("图片中不包含“赞助内容”四个字")   
                        time.sleep(3)
                        # 点击评论区
                        comment_id_x = random.randint(983, 1027)
                        comment_id_y = random.randint(1320, 1390)
                        fb_tap_point(udid, comment_id_x, comment_id_y)
                        print(f"[{udid}] 评论区已打开")
                        time.sleep(2)  # 内容加载

                        # 截图评论区
                        screenshot_path = f"/sdcard/comments_{udid}.png"
                        local_path = f"E:\\代码截图temp\\comments_{udid}.png"
                        subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', screenshot_path], check=True)
                        subprocess.run(['adb', '-s', udid, 'pull', screenshot_path, local_path], check=True)
                        print(f"[{udid}] 评论区截图已保存到本地：{local_path}")

                        # 将截图转换为Base64
                        base64_data = fb_convert_image_to_base64(local_path)
                        print(f"[{udid}] 评论区截图已转换为Base64")
                        image = fb_decode_base64_to_image(base64_data)
                        if image is None:
                            print("图片解码失败，程序终止。")
                            return

                        # 预处理图像
                        processed_image = fb_preprocess_image(image)

                        # OCR 提取文本
                        extracted_text = fb_extract_text_from_image(processed_image)

                        # 解析评论
                        comments = fb_parse_comments(extracted_text)

                        # 打印评论
                        print("提取的评论内容：")
                        for idx, comment in enumerate(comments, 1):
                            print(f"{idx}. {comment}")
                        # 评论区滑动
                        up_swipes = random.randint(2, 5)
                        down_swipes = random.randint(1, 5)
                        print(f"[{udid}] 上下滑动次数: {up_swipes}次, {down_swipes}次")
                        # 获取评论信息

                        # 关闭评论区
                        print(f"[{udid}] 关闭评论区")
                        fb_press_back(udid)#返回
                        time.sleep(1)
                        # 双击屏幕点赞
                        randomclick_number = random.randint(1, 9)
                        print(f"[{udid}] 随机生成的数是: {randomclick_number}")
                        if randomclick_number % 2 == 0:
                            print(f"[{udid}] 随机数为偶数，执行双击点赞操作")
                            fb_double_tap_like(udid)
                        else:
                            print(f"[{udid}] 随机数为奇数，跳过双击点赞操作")
                        # 随机选择是否点关注
                        random_number = random.randint(1, 9)
                        print(f"[{udid}] 随机生成的数是: {random_number}")
                        if random_number % 2 == 0:
                            print(f"[{udid}] 随机数为偶数，执行点击关注操作")
                        else:
                            print(f"[{udid}] 随机数为奇数，跳过关注操作")
                        # 计算并执行总等待时间
                        extra_wait_time = random.randint(1, 10)
                        total_wait_time = base_wait_time + extra_wait_time
                        print(f"[{udid}] 总等待时间: {total_wait_time}秒")
                        time.sleep(total_wait_time)
                else:
                    print(f"[{udid}] isInterested为False,等待{base_wait_time}秒")
                    time.sleep(base_wait_time)
                    fb_swipe_to_next_video(udid)

                    # 如果不是最后一次循环，执行滑动
                    if i < slide - 1:
                        print(f"[{udid}] 滑动到下一个视频")
                        start_next_x = random.randint(460, 1000)
                        end_next_x = random.randint(540, 840)
                        start_next_y = 1650
                        end_next_y = 540

                        fb_human_swipe(udid, start_next_x, start_next_y, end_next_x, end_next_y,
                                    duration=random.randint(250, 350))
                        time.sleep(random.uniform(0.5, 2))

            except Exception as e:
                print(f"[{udid}] 操作发生错误: {e}")
                return False

        print(f"[{udid}] 所有滑动操作完成")
        # 关闭应用
        fb_close_facebook(udid)
        return True

    except Exception as e:
        print(f"[{udid}] Facebook 操作失败: {e}")
        try:
            fb_close_facebook(udid)
        except Exception as close_error:
            print(f"[{udid}] 关闭应用失败: {close_error}")
        return False

"""模拟返回按键操作"""
def fb_press_back(udid):
    try:
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_BACK'], check=True)
        print(f"[{udid}] 模拟返回按键成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[{udid}] 模拟返回按键失败: {e}")
        return False

"""返回手机桌面"""
def fb_back_to_home(udid):
    try:
        print(f"[{udid}] 正在返回桌面...")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
        time.sleep(1)
        print(f"[{udid}] 已返回桌面")
        return True
    except Exception as e:
        print(f"[{udid}] 返回桌面失败: {e}")
        return False

"""点击指定坐标"""
def fb_tap_point(udid, x, y):
    try:
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'tap', str(x), str(y)])
        time.sleep(0.5)  # 等待点击响应
        return True
    except Exception as e:
        print(f"[{udid}] 点击失败: {e}")
        return False

"""关闭 Facebook 应用并返回桌面"""
def fb_close_facebook(udid):
    try:
        print(f"[{udid}] 正在关闭 Facebook...")
        # 强制停止 Facebook 应用
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'am', 'force-stop', 'com.facebook.katana'
        ], check=True)
        time.sleep(1)

        # 返回桌面
        fb_back_to_home(udid)
        print(f"[{udid}] Facebook 已关闭并返回桌面")
        return True
    except Exception as e:
        print(f"[{udid}] 关闭 Facebook 失败: {e}")
        return False

"""处理单个设备的所有操作流程"""
def fb_process_device(udid):
    import pytesseract
    # 显式设置路径
    pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\tesseract.exe"
    try:
        print(f"\n开始处理设备 {udid}")
        status = fb_check_device_status(udid)
        if status:
            print(f"设备 {udid} 状态:")
            print(f"- 连接状态: {'已连接' if status['connected'] else '未连接'}")
            print(f"- 屏幕状态: {'已亮起' if status['screen_on'] else '已关闭'}")
            print(f"- 电池电量: {status['battery_level']}%")
            print(f"- WiFi状态: {'已连接' if status['wifi_connected'] else '未连接'}")

            if not status['screen_on']:
                fb_ensure_screen_unlocked(udid)

            # 先返回桌面
            fb_back_to_home(udid)
            time.sleep(1)

            # 打开 Facebook 并执行操作
            fb_open_facebook(udid)
    except Exception as e:
        print(f"[{udid}] 设备处理过程出错: {e}")

"""将 Base64 解码为图片"""
def fb_decode_base64_to_image(base64_string):
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        print(f"解码 Base64 数据失败: {e}")
        return None

"""图像预处理（可选，增强 OCR 识别准确度）"""
def fb_preprocess_image(image):
    try:
        # 裁剪评论区域（根据截图调整坐标）
        cropped_image = image.crop((0, 400, image.width, image.height - 100))  # 调整为实际评论区
        # 转为灰度图像
        gray_image = cropped_image.convert("L")
        # 去噪声处理
        np_image = np.array(gray_image)
        denoised_image = cv2.fastNlMeansDenoising(np_image, None, 30, 7, 21)
        # 增强对比度
        enhancer = ImageEnhance.Contrast(Image.fromarray(denoised_image))
        enhanced_image = enhancer.enhance(2.0)
        # 自适应二值化
        binary = cv2.adaptiveThreshold(
            np.array(enhanced_image), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        # 转换回 PIL 格式供 OCR 使用
        return Image.fromarray(binary)
    except Exception as e:
        print(f"图像预处理失败: {e}")
        return image


"""提取评论内容"""
def fb_extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image, lang="eng+chi_sim+jpn")
        print("OCR 提取的原始文本内容：")
        print(text)
        return text
    except Exception as e:
        print(f"OCR 文字提取失败: {e}")
        return ""


"""解析评论信息"""
def fb_parse_comments(text):
    lines = text.split("\n")
    comments = []
    current_user = None
    current_comment = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测用户名（假设用户名后跟冒号或是换行）
        user_match = re.match(r"^([A-Za-z0-9_.-]+):?$", line)
        if user_match:
            if current_user and current_comment:
                comments.append(f"{current_user}: {current_comment.strip()}")
            current_user = user_match.group(1)
            current_comment = ""
        else:
            # 合并到当前评论
            current_comment += f" {line}"

    # 添加最后一条评论
    if current_user and current_comment:
        comments.append(f"{current_user}: {current_comment.strip()}")

    return comments

"""在视频中心区域随机选择一个点进行双击"""
def fb_double_tap_like(udid):
    try:
        center_x = random.randint(300, 800)  # 视频中心区域X轴范围
        center_y = random.randint(800, 1200)  # 视频中心区域Y轴范围

        print(f"[{udid}] 执行双击点赞操作，位置：({center_x}, {center_y})")

        # 执行双击，两次点击间隔要短
        fb_tap_point(udid, center_x, center_y)
        time.sleep(0.05)  # 减少两次点击之间的间隔
        fb_tap_point(udid, center_x, center_y)

        print(f"[{udid}] 双击点赞完成")
        return True
    except Exception as e:
        print(f"[{udid}] 双击点赞失败: {e}")
        return False

if __name__ == "__main__":
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\tesseract.exe"
    # 获取所有连接的设备
    devices = fb_get_connected_devices()
    if not devices:
        print("没有检测到连接的设备")
    else:
        print(f"检测到 {len(devices)} 台设备，开始并行处理")

        # 创建线程列表
        threads = []

        # 为每个设备创建并启动一个单独线程
        for udid in devices:
            thread = threading.Thread(
                target=fb_process_device,
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
