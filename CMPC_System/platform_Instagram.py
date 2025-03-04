#!/usr/bin/env python
# -- coding: utf-8 --
import subprocess
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
import logging
import subprocess
import time
import random
import cv2
import numpy as np
import pytesseract
from io import BytesIO
import numpy as np
import xml.etree.ElementTree as ET
from io import BytesIO
import string  # 添加到其他 import 语句部分


# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

def setup_logging():
    """配置日志系统"""
    try:
        # 创建日志目录
        log_directory = r"E:\PycharmProjects\genesis_start\CMPC_System\logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        
        # 生成带时间戳的日志文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file_path = os.path.join(log_directory, f'instagram_{timestamp}.log')
        
        # 配置日志格式
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # 获取根日志记录器并配置
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # 清除现有的处理器
        logger.handlers.clear()
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logging.info(f"日志系统初始化完成，日志文件：{log_file_path}")
        
    except Exception as e:
        print(f"设置日志系统时出错: {e}")
        raise


def check_live_stream(udid):
    """
    检查当前页面是否包含直播内容
    返回: bool
    """
    try:
        # 使用UIAutomator dump当前界面
        dump_result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            timeout=5  # 添加超时限制
        )

        # 将xml文件拉到本地
        pull_result = subprocess.run(
            ['adb', '-s', udid, 'pull', '/data/local/tmp/ui.xml', f'temp_{udid}.xml'],
            check=True,
            timeout=5  # 添加超时限制
        )

        # 读取xml文件内容
        tree = ET.parse(f'temp_{udid}.xml')
        root = tree.getroot()

        # 扩展直播相关的关键词列表
        live_keywords = [
            'LIVE', 'LIVE now', 'Tap to watch LIVE'
        ]

        # 检查所有可能包含文本的节点
        text_nodes = root.findall(".//node[@text]")
        for node in text_nodes:
            text = node.get('text', '').strip()
            if any(keyword.lower() in text.lower() for keyword in live_keywords):
                print(f"[{udid}] 检测到直播内容标识: {text}")
                return True

        return False

    except subprocess.TimeoutExpired:
        print(f"[{udid}] 检查直播内容超时")
        return False
    except Exception as e:
        print(f"[{udid}] 检查直播内容时出错: {e}")
        return False
    finally:
        # 清理临时文件
        try:
            if os.path.exists(f'temp_{udid}.xml'):
                os.remove(f'temp_{udid}.xml')
            subprocess.run(
                ['adb', '-s', udid, 'shell', 'rm', '/data/local/tmp/ui.xml'],
                timeout=3
            )
        except Exception as e:
            print(f"[{udid}] 清理临时文件失败: {e}")

def input_text(udid, text):
    """使用直接的adb shell input text 命令输入文本，并模拟人工输入速度"""
    try:
        print(f"[{udid}] 输入文本: {text}")
        input_box_x = random.randint(330, 330)
        input_box_y = random.randint(189, 235)
        tap_point(udid, input_box_x, input_box_y)
        time.sleep(0.5)
        
        # 清除现有文本
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'keyevent', 'KEYCODE_CLEAR'], check=True)
        time.sleep(1)

        # 将文本分成单个字符，并添加随机延迟
        for char in text:
            
            if char in [' ', '"', "'", '\\', '(', ')', '[', ']', '{', '}', '$', '&', '*', '<', '>', '|']:
                escaped_char = f"\\{char}"
            else:
                escaped_char = char
                
            # 输入单个字符
            cmd = f'adb -s {udid} shell input text "{escaped_char}"'
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[{udid}] 输入字符 '{char}' 失败: {e}")
                raise

            # 添加随机延迟，模拟人工输入速度
            delay = random.uniform(0.2, 1)  # 每个字符之间添加0.2-1秒的随机延迟
            time.sleep(delay)
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
            # 提取电池电量数值
            for line in battery_result.stdout.splitlines():
                if 'level' in line:
                    battery_level = int(line.split(':')[1].strip())
                    status['battery_level'] = battery_level
                    break

            # 检查WiFi连接
            wifi_cmd = "dumpsys wifi | grep 'Wi-Fi is'"
            wifi_result = subprocess.run(['adb', '-s', udid, 'shell', wifi_cmd],
                                         stdout=subprocess.PIPE, text=True)
            status['wifi_connected'] = 'enabled' in wifi_result.stdout.lower()

        return status
    except Exception as e:
        print(f"[{udid}] 检查设备状态失败: {e}")
        return None


def base64_to_temp_image_file(base64_data, temp_path="temp_keyword_image.png"):
    """
    将Base64数据解码并写入临时文件，返回临时图片文件路径
    """
    try:
        # 如果开头含 data:image/png;base64, 等类似前缀，则剥离
        if base64_data.startswith("data:image/"):
            base64_data = base64_data.split(",", 1)[-1]

        image_bytes = base64.b64decode(base64_data)
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        return temp_path
    except Exception as e:
        print(f"将 Base64 转为临时文件失败: {e}")
        return None

#截图并转为base64返回
# def get_screenshot_base64(udid):
#     try:
#         logging.info(f"[{udid}] 开始截图")
#         subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'], check=True)
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
#         device_filename = f"/data/local/tmp/screen_{timestamp}.png"
#         subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', device_filename], check=True)
#         result = subprocess.run(
#             ['adb', '-s', udid, 'shell', 'cat', device_filename],
#             stdout=subprocess.PIPE,
#             check=True
#         )
#         logging.debug(f"[{udid}] 原始数据长度: {len(result.stdout)}")
#         base64_data = base64.b64encode(result.stdout).decode('utf-8')
#         logging.debug(f"[{udid}] Base64数据长度: {len(base64_data)}")
#         subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', device_filename], check=True)
#         return base64_data
#     except Exception as e:
#         logging.error(f"[{udid}] 截图失败: {e}")
#         try:
#             subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'])
#         except:
#             pass
#         return None
def get_screenshot_base64(udid):
    """
    获取设备截图并转换为base64，优化打印和清理逻辑
    """
    try:
        print(f"[{udid}] 开始执行截屏操作...")

        # 清理设备上的旧截图
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', '/data/local/tmp/screen*.png'], check=True)

        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        device_filename = f"/data/local/tmp/screen_{timestamp}.png"
        local_filename = f"temp_{udid}_{timestamp}.png"

        # 截取屏幕并传输
        subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', device_filename], check=True)
        subprocess.run(['adb', '-s', udid, 'pull', device_filename, local_filename], check=True)

        # 转换为 Base64
        with open(local_filename, 'rb') as image_file:
            base64_data = base64.b64encode(image_file.read()).decode('utf-8')

        # 打印摘要信息，避免长字符串干扰
        print(f"[{udid}] 截图转换完成，Base64长度: {len(base64_data)}")
        # 清理临时文件
        os.remove(local_filename)
        subprocess.run(['adb', '-s', udid, 'shell', 'rm', '-f', device_filename], check=True)

        return base64_data
    except Exception as e:
        print(f"[{udid}] 截图失败: {e}")
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
    模拟人类的滑动操作，生成一个平滑的滑动轨迹
    参数:
    - udid: 设备ID
    - start_x, start_y: 起始坐标
    - end_x, end_y: 结束坐标
    - duration: 滑动持续时间(毫秒)
    """
    try:
        # 使用单次 swipe 命令完成整个滑动
        subprocess.run(
            ['adb', '-s', udid, 'shell', 'input', 'swipe',
             str(start_x), str(start_y), str(end_x), str(end_y), str(duration)],
            check=True, timeout=5
        )
        return True

    except Exception as e:
        print(f"[{udid}] 人工滑动模拟失败: {e}")
        return False

def mock_api_response():
    """模拟API响应，随机返回True或False"""
    # is_interested = random.choice([True, False])
    is_interested = True
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

def tk_extract_text_from_base64(base64_data, min_length=30):
    """
    从 Tiktok Base64 数据中提取评论信息，并过滤掉长度小于 min_length 的评论
    """
    # 解码base64
    image_data = base64.b64decode(base64_data)
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用Tesseract进行OCR
    text = pytesseract.image_to_string(gray, lang='eng', config='--psm 6')

    # 过滤评论内容
    comments = []
    for line in text.split('\n'):
        # 去掉空行和含有无关关键字的行
        if line.strip() and not any(keyword in line.lower() for keyword in ["search", "like", "reply"]):
            # 只保留长度大于等于 min_length 的行
            if len(line.strip()) >= min_length:
                comments.append(line.strip())

    return comments


def extract_comments_from_base64(base64_data):
    """
    从instagram Base64 数据中提取评论信息
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

        # 获取截图的Base64编码
        base64_data = get_screenshot_base64(udid)
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

"""API接口返回人设搜索关键字内容"""
def get_search_keyword(udid, profile):
    """获取人设搜索关键字内容"""
    url = 'https://iris.iigood.com/iris/v1/agent/keywords'
    payload = {
        "profile": profile,
        "lang":"english"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[{udid}] get_search_keyword请求返回: {response.json()}")
        if response.status_code == 200:
            data = response.json()
            keywords = data.get("keywords", [])
            if keywords:
                # 随机选择一个关键词
                selected_keyword = random.choice(keywords)
                print(f"[{udid}] 随机选择的关键词: {selected_keyword}")
                return selected_keyword
            else:
                print(f"[{udid}] 没有可用的关键词")
                return None
        else:
            print(f"[{udid}] 请求失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[{udid}] 获取人设搜索关键字失败: {e}")
        return None
    
"""发布文案生成"""
def copywriting_release(udid,profile):
    """发布文案生成"""
    url = 'https://iris.iigood.com/iris/v1/agent/copywriting'
    payload = {
        "content": profile,
        "platform":"instagram"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[{udid}] copywriting_release请求返回: {response.json()}")
        if response.status_code == 200:
            data = response.json()
            copywriting = data.get("copywriting", "")
            return copywriting
        else:
            print(f"[{udid}] 请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"[{udid}] 获取发布文案失败: {e}")
        return None

#动态识别页面的文字信息点击对应坐标
def tap_on_text(udid, target_texts):
    """根据页面上的文字点击相应的坐标"""
    try:
        # 截取当前屏幕
        screenshot_path = f"/sdcard/screen_{udid}.png"
        local_path = f"screen_{udid}.png"
        subprocess.run(['adb', '-s', udid, 'shell', 'screencap', '-p', screenshot_path], check=True)
        subprocess.run(['adb', '-s', udid, 'pull', screenshot_path, local_path], check=True)

        # 使用OCR识别文字
        img = cv2.imread(local_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data = pytesseract.image_to_data(gray, lang='chi_sim', output_type=pytesseract.Output.DICT)

        # 遍历识别结果，寻找目标文字
        for i, text in enumerate(data["text"]):
            if text in target_texts:
                x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                center_x, center_y = x + w // 2, y + h // 2
                print(f"找到目标文字 '{text}'，点击坐标: ({center_x}, {center_y})")
                tap_point(udid, center_x, center_y)
                return True

        print(f"未找到目标文字: {target_texts}")
        return False

    except Exception as e:
        print(f"点击目标文字失败: {e}")
        return False

"""首页发布视频点击加号"""
def viode_release(udid,profile):
    Video_release_x = random.randint(480,560)
    Video_release_y = random.randint(2025,2068)
    tap_point(udid, Video_release_x, Video_release_y)
    print(f"[{udid}] 点击加号按钮")
    time.sleep(3)

    #默认选中第一条视频继续
    Confirmation_Video_x = random.randint(110,290)
    Confirmation_Video_y = random.randint(680,850)
    tap_point(udid, Confirmation_Video_x, Confirmation_Video_y)
    time.sleep(3)

    #选中视频后点击右下角继续按钮
    Next_step_x = random.randint(850,980)
    Next_step_y = random.randint(2015,2056)
    tap_point(udid, Next_step_x, Next_step_y)
    time.sleep(3)
    #点击右下角继续下一步确认，进入到视频文案编辑页面
    Next_step_x = random.randint(850,980)
    Next_step_y = random.randint(2015,2056)
    tap_point(udid, Next_step_x, Next_step_y)
    time.sleep(3)
    
    #根据页面文案关键字识别输入框准确坐标
    target_texts = ["Write a caption"]
    tap_on_text(udid, target_texts)
    time.sleep(5)
    """发布视频的配文文案"""
    copywriting = copywriting_release(udid,profile)
    print(f"[{udid}] 发布视频的配文文案: {copywriting}")
    input_text(udid, text=copywriting)
    time.sleep(1)
    #点击确认按钮分享发布
    Next_step_x = random.randint(935,998)
    Next_step_y = random.randint(188,200)
    tap_point(udid, Next_step_x, Next_step_y)
    time.sleep(15)

def open_tiktok(udid):
    """打开 Tiktok 应用，进行Tiktok的一系列操作"""

    # 启动 TikTok 应用
    try:    
        subprocess.run([
            'adb', '-s', udid, 'shell',
            'am', 'start', '-n',
            'com.zhiliaoapp.musically/com.ss.android.ugc.aweme.splash.SplashActivity'
        ])
        time.sleep(5)  # 等待应用启动
        print(f"[{udid}] TikTok 已启动")
    except Exception as e:
        print(f"[{udid}] 启动 TikTok 失败: {e}")

    #启动成功之后，后续操作流程
    """
    1. 首页滑动视频
    2. 兴趣视频双击点赞操作
    3. 点击允许按钮
    4. 点击允许按钮
    5. 点击允许按钮
    6. 点击允许按钮
    7. 点击允许按钮
    """
    #自定义视频观看次数
    slide = 2
    for i in range(slide): 
        if not check_device_status(udid):
            try:
                print(f"[{udid}] 设备断开，重新连接")
                subprocess.run(['adb', '-s', udid, 'connect'])
                time.sleep(1)
            except Exception as e:
                print(f"[{udid}] 设备断开，重新连接失败: {e}")
                return      
        print(f"进行第{i+1}次滑动")
        try:
            #获取截图转换为Base64
            base64_data = get_screenshot_base64(udid)
            if not base64_data:
                print(f"[{udid}] 获取截图失败")
                continue
            
            if check_live_stream(udid):
                    print(f"[{udid}] 跳过直播内容")
                    # 在 check_live_stream 检测到直播内容后的滑动操作前添加
                    swipe_coords = [
                        random.randint(460, 850),  # start_x
                        1650,                      # start_y
                        random.randint(540, 840),  # end_x
                        1020                       # end_y
                    ]
                    subprocess.run(
                        ['adb', '-s', udid, 'shell', 'input', 'swipe'] +
                        [str(x) for x in swipe_coords] + ['300'],
                        check=True, timeout=5
                    )
                    time.sleep(random.uniform(1, 2))
                    continue

            api_response = mock_api_response()
            print(f"[{udid}] 模拟 API 响应: {api_response}")
            #设置基础等待时间
            base_wait_time = random.randint(2, 7)
            time.sleep(base_wait_time)

            #根据API返回结果判断是否感兴趣
            if api_response and isinstance(api_response, dict) and api_response.get('isInsterested') == True:
                #等待基础时间
                time.sleep(base_wait_time)
                #打开评论区
                comment_id_x = random.randint(981, 1000)
                comment_id_y = random.randint(1643, 1700)
                tap_point(udid, comment_id_x, comment_id_y)
                time.sleep(2)
                #准备获取tiktok评论区信息
                #获取评论区截图
                base64_data_play = get_screenshot_base64(udid)
                #提取评论区信息
                comments = tk_extract_text_from_base64(base64_data_play)
                if comments:
                    print(f"[{udid}] 获取到{len(comments)}条评论")
                    for idx, comment in enumerate(comments, 1):
                        print(f"{idx}.{comment}")

                #评论区滑动3
                up_swipes = random.randint(1,3)
                down_swipes = random.randint(1,2)
                print(f"[{udid}] 上下滑动次数: {up_swipes}次, {down_swipes}次")

                time.sleep(2)

                #点击空白处关闭评论区
                blank_x = random.randint(300, 800)
                blank_y = random.randint(375, 600)
                tap_point(udid, blank_x, blank_y)
                time.sleep(1)   
                #点赞判断
                if random.randint(1, 9) % 2 == 0:
                    print(f"[{udid}] 随机数为偶数，执行双击点赞操作")
                    tap_point(udid, 500, 1500)
                    time.sleep(0.5)
                    tap_point(udid, 490, 1500)
                else:
                    print(f"[{udid}] 随机数为奇数，跳过双击点赞操作")   


                #计算视频总停留时间
                long_wait_time = random.randint(10, 30)+base_wait_time
                time.sleep(long_wait_time)
                print(f"[{udid}] 视频总停留时间: {long_wait_time}秒")
                #滑动到下一个视频
                if i < slide - 1:
                    print(f"[{udid}] 滑动到下一个视频")
                    start_next_x = random.randint(460, 850)
                    end_next_x = random.randint(540, 840)
                    start_next_y = 1650
                    end_next_y = 1020
                    human_swipe(udid, start_next_x, start_next_y, end_next_x, end_next_y, duration=random.randint(250, 350))
                    time.sleep(random.uniform(1, 2))

            else:
                print(f"{udid}返回为False，默认等待{base_wait_time}秒")
                print(f"[{udid}] 不感兴趣，跳过")
                if i < slide - 1:
                    print(f"[{udid}] 滑动到下一个视频")
                    start_next_x = random.randint(460, 850)
                    end_next_x = random.randint(540, 840)
                    start_next_y = 1650
                    end_next_y = 1020
                    human_swipe(udid, start_next_x, start_next_y, end_next_x, end_next_y, duration=random.randint(250, 350))
                    time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"[{udid}] 获取截图失败: {e}")
            continue
    
    # 在最后添加关闭应用和返回桌面的逻辑
    try:
        # 强制停止 TikTok 应用
        print(f"[{udid}] 正在关闭 TikTok...")
        
        # 返回桌面
        back_to_home(udid)
        print(f"[{udid}] TikTok 已关闭并返回桌面")
    except Exception as close_error:
        print(f"[{udid}] 关闭 TikTok 或返回桌面时出错: {close_error}")

"""打开 Instagram 应用，进行Instagram的一系列操作"""
def open_instagram(udid):
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
        time.sleep(3)
        #场景描述
        #copywriting_profile = "The feeling of reuniting with friends at a gathering after a long time apart."
        #调用视频发布
        # copywriting = viode_release(udid,copywriting_profile)
        # print(f"[{udid}] 发布视频的配文文案: {copywriting}")
        # input_text(udid, text=copywriting)
        # time.sleep(1)

        #回到首页
        # bank_home_x = random.randint(75, 125)
        # bank_home_y = random.randint(2020, 2100)
        # tap_point(udid, bank_home_x, bank_home_y)
        #首页搜索按钮图标坐标
        search_id_x = random.randint(273, 310)
        search_id_y = random.randint(2261, 2296)

        #点击搜索输入框
        search_count_x = random.randint(305, 528)
        search_count_y = random.randint(190, 220)

        #确认搜索按钮坐标
        confirm_id_x = random.randint(951,1010)
        confirm_id_y = random.randint(2129,2200)

         #搜索结果页面
        up_swipes = random.randint(1, 3)
        down_swipes = random.randint(1, 3)

        #点击搜索按钮，弹出输入框
        print(f"点击搜索按钮：（{search_id_x},{search_id_y}）")
        tap_point(udid, search_id_x, search_id_y)
        time.sleep(1)

        #点击搜索框
        tap_point(udid, search_count_x, search_count_y)
        time.sleep(1)
         #关键词请求人设
        keyword_profile = "I am a 30-year-old young father who enjoys gourmet food, beautiful cars, and outdoor adventures, and I often take care of my children at home on weekends."
        #调用人设生成关键词方法，获取搜索关键词
        input_keyword = get_search_keyword(udid,keyword_profile)
        time.sleep(5)

        #输入搜索关键词
        input_text(udid, text=input_keyword)
        time.sleep(1)

        #点击确认搜索按钮
        tap_point(udid, confirm_id_x, confirm_id_y)
        time.sleep(5)
        #从右往左滑动显示reels按钮
        start_hz_x = random.randint(900, 980)
        end_hz_x = random.randint(280, 450)
        start_hz_y = 357  # 下部区域
        end_hz_y = 320    # 上部区域
        human_swipe(udid, start_hz_x, start_hz_y, end_hz_x, end_hz_y, duration=500)

         #切换视频板块Reels
        key_reels= "Reels"
        base64_data = get_screenshot_base64(udid)
        reels_id_x, reels_id_y = find_keyword_coordinates(base64_data, key_reels)
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
            end_y = 800    # 上部区域
            
            # 使用人工滑动
            human_swipe(udid, start_x, start_y, end_x, end_y, 
                        #滑动区间随机，模拟人类真实行为
                        duration=random.randint(250, 350))
            time.sleep(random.uniform(1, 3))

        for _ in range(down_swipes):
            # 生成随机的起点和终点坐标，保持在区域内
            start_x = random.randint(120, 970)
            end_x = random.randint(120, 970)
            start_y = 1000    # 上部区域
            end_y = 1800    # 下部区域
            
            # 使用人工滑动
            human_swipe(udid, start_x, start_y, end_x, end_y, 
                        duration=random.randint(250, 350))
            time.sleep(random.uniform(0.5, 2))

        # 随机等待一下，模拟人工浏览
        time.sleep(random.uniform(1, 3))

        # 在限定区域内随机选择一个点击位置
        random_click_x = random.randint(130, 950)
        random_click_y = random.randint(650, 976)
        
        print(f"[{udid}] 在搜索结果页面随机点击位置: ({random_click_x}, {random_click_y})")
        tap_point(udid, random_click_x, random_click_y)
        time.sleep(2)  # 等待内容加载
        
        # 继续执行后续的视频滑动操作...
        slide = 2
        api_url = "https://iris.iigood.com/iris/v1/agent/interest"

        # 开始循环滑动视频
        for i in range(slide):
            #每次检查设备是否还连接，如果断开，则重新连接
            if not check_device_status(udid):
                try:
                    print(f"[{udid}] 设备断开，重新连接")
                    subprocess.run(['adb', '-s', udid, 'connect'])
                    time.sleep(1)
                except Exception as e:
                    print(f"[{udid}] 设备断开，重新连接失败: {e}")
                    return
            
            print(f"进行第{i+1}次滑动")
            try:
                #获取截图转换为Base64(等朱江伟接口开放，目前走mock逻辑)
                # base64_data = get_screenshot_base64(udid)
                # if not base64_data:
                #     print(f"[{udid}] 获取截图失败")
                #     continue

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
                    comment_id_x = random.randint(980, 990)
                    comment_id_y = random.randint(1643, 1700)
                    tap_point(udid, comment_id_x, comment_id_y)
                    print(f"[{udid}] 评论区已打开")
                    time.sleep(2)  # 内容加载

                    # 评论区滑动
                    up_swipes = random.randint(1,3)
                    down_swipes = random.randint(1,2)
                    print(f"[{udid}] 上下滑动次数: {up_swipes}次, {down_swipes}次")
                    
                    # 在评论区滑动
                    for _ in range(up_swipes):
                        # 生成随机的起点和终点坐标，保持在评论区域内
                        start_x = random.randint(520, 560)  # 在中心区域随机
                        end_x = random.randint(520, 560)
                        start_y = 1800  # 下部区域
                        end_y = 1000    # 上部区域
                        
                        # 使用人工滑动
                        human_swipe(udid, start_x, start_y, end_x, end_y, 
                                    duration=random.randint(250, 350))
                        time.sleep(random.uniform(0.5, 2))

                    for _ in range(down_swipes):
                        # 生成随机的起点和终点坐标，保持在评论区域内
                        start_x = random.randint(520, 560)
                        end_x = random.randint(520, 560)
                        start_y = 1000    # 上部区域
                        end_y = 1800    # 下部区域
                        
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
                    #双击屏幕点赞
                    randomclick_number = random.randint(1, 9)
                    print(f"[{udid}] 随机生成的数是: {randomclick_number}")
                    if randomclick_number % 2 == 0:
                        print(f"[{udid}] 随机数为偶数，执行双击点赞操作")
                        tap_point(udid, 500, 1500)
                        time.sleep(0.1)
                        tap_point(udid, 500, 1500)
                    else:
                        print(f"[{udid}] 随机数为奇数，跳过双击点赞操作")
                    #随机选择是否点关注
                    random_number = random.randint(1, 9)
                    print(f"[{udid}] 随机生成的数是: {random_number}")
                    if random_number % 2 == 0:
                        print(f"[{udid}] 随机数为偶数，执行点击关注操作")
                        key_follow= "Follow"
                        #获取截图转换为Base64
                        print(f"[{udid}] 开始执行截屏操作...")  
                        click_keyword_base64_data = get_screenshot_base64(udid)
                        click_x, click_y = find_keyword_coordinates(click_keyword_base64_data, key_follow)
                        tap_point(udid, click_x, click_y)
                    else:
                        print(f"[{udid}] 随机数为奇数，跳过关注操作")

                    # 计算并执行总等待时间
                    extra_wait_time = random.randint(1, 60)
                    total_wait_time = base_wait_time + extra_wait_time
                    print(f"[{udid}] 总等待时间: {total_wait_time}秒")
                    time.sleep(total_wait_time)
                    
                    #等待结束，滑动到下一个视频
                    if i < slide - 1:
                        print(f"[{udid}] 滑动到下一个视频")
                        start_next_x = random.randint(460, 1000)
                        end_next_x = random.randint(540, 840)
                        start_next_y = 1650
                        end_next_y = 540
                        
                        human_swipe(udid, start_next_x, start_next_y, end_next_x, end_next_y, 
                                    duration=random.randint(250, 350))
                        time.sleep(random.uniform(0.5, 2))
                else:
                    print(f"[{udid}] isInterested为False,等待{base_wait_time}秒")
                    time.sleep(base_wait_time)
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

"""接收关键字并返回坐标"""
def find_keyword_coordinates(base64_data, keyword):
    """
    从 Base64 图像数据中找到关键字的坐标
    """
    try:
        # 解码 Base64 数据为图像
        image_data = base64.b64decode(base64_data)
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print("无法解码 Base64 数据为图像")
            return None

        # 转灰度
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 预处理图像（可选）：二值化
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # OCR 识别文字及坐标
        data = pytesseract.image_to_data(binary, lang='chi_sim', output_type=pytesseract.Output.DICT)

        # 遍历 OCR 数据，查找关键字
        for i, text in enumerate(data["text"]):
            if keyword in text:
                x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                center_x, center_y = x + w // 2, y + h // 2
                print(f"找到关键字 '{keyword}'，坐标: ({center_x}, {center_y})")
                return (center_x, center_y)

        print(f"未找到关键字 '{keyword}'")
        return None

    except Exception as e:
        print(f"find_keyword_coordinates 错误: {e}")
        return None


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
        time.sleep(2)  # 等待点击响应
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
            #open_instagram(udid)
            open_tiktok(udid)
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
    setup_logging()
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