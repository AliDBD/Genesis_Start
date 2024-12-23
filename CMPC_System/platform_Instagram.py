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

def open_instagram(udid):
    """打开 Instagram 应用"""
    try:
        print(f"[{udid}] 正在打开 Instagram...")
        
        # 先强制停止 Instagram 应用
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

        #首页搜索按钮图标坐标
        search_id_x = random.randint(295, 372)
        search_id_y = random.randint(2045, 2103)

        #确认搜索按钮坐标
        confirm_id_x = random.randint(930,1010)
        confirm_id_y = random.randint(2020,2090)

        print(f"点击搜索按钮：（{search_id_x},{search_id_y}）")
        tap_point(udid, search_id_x, search_id_y)
        time.sleep(1)
        input_text(udid,text="wig")#输入搜索文本
        tap_point(udid,confirm_id_x,confirm_id_y)

        slide = 2
        api_url = "https://iris.iigood.com/iris/v1/agent/interest"
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
                #获取截图转换为Base64
                base64_data = get_screenshot_base64(udid)
                if base64_data:
                    #发送到API，设置时间等待为10秒
                    api_response = send_screenshot_to_api(base64_data, api_url, udid)
                    print(f"[{udid}] API 响应: {api_response}")

                    #设定基础等待时间
                    time.sleep(3)
                    #根据API返回结果中的isInsterested判断是否感兴趣
                    if api_response and isinstance(api_response, dict) and api_response.get('isInsterested') == True:
                        time.sleep(3)
                        #点击评论区坐标按钮
                        comment_id_x = random.randint(950, 1015)
                        comment_id_y = random.randint(1365, 1450)
                        tap_point(udid, comment_id_x, comment_id_y)
                        print(f"[{udid}] 评论区已打开")
                        time.sleep(2)#内容加载

                        #获取评论区评论内容
                        comments = get_comments_ui(udid)
                        if comments:
                            print(f"[{udid}] 获取到{len(comments)}条评论")
                            for i, comment in enumerate(comments, 1):
                                print(f"{i}.{comment}")
                            #发送评论到API
                            comments_api_url = "https://iris.iigood.com/iris/v1/agent/comment"
                            comments_response = send_comments_to_api(comments, udid, comments_api_url)
                            if comments_response:
                                print(f"[{udid}] 评论API返回: {comments_response}")

                        #随机决定上下滑动次数
                        up_swipes = random.randint(2,5)
                        down_swipes = random.randint(1,5)
                        print(f"[{udid}] 上下滑动次数: {up_swipes}次, {down_swipes}次")
                        #在评论区滑动
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
                        #关闭评论区
                        tap_point(udid, 1000, 1000)
                        time.sleep(1)
                    else:
                        print(f"[{udid}] 未感兴趣")
            except Exception as e:
                print(f"[{udid}] 设备断开，重新连接失败: {e}")
                return False


        return True


    except Exception as e:
        print(f"[{udid}] 打开 Instagram 失败: {e}")
        return False

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
        print(f"[{udid}] 点击坐标: ({x}, {y})")
        subprocess.run(['adb', '-s', udid, 'shell', 'input', 'tap', str(x), str(y)])
        time.sleep(0.5)  # 等待点击响应
        return True
    except Exception as e:
        print(f"[{udid}] 点击失败: {e}")
        return False

def perform_instagram_actions(udid):
    """执行 Instagram 的一系列操作"""
    try:
        print(f"[{udid}] 开始执行 Instagram 操作流程...")
        
        print(f"[{udid}] Instagram 操作流程完成")
        return True
    except Exception as e:
        print(f"[{udid}] Instagram 操作失败: {e}")
        return False

def process_device(udid):
    """处理单个设备的所有操作流程"""
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
            if open_instagram(udid):
                perform_instagram_actions(udid)
    except Exception as e:
        print(f"[{udid}] 设备处理过程出错: {e}")

if __name__ == "__main__":
    # 获取所有连接的设备
    devices = get_connected_devices()
    if not devices:
        print("没有检测到连接的设备")
    else:
        print(f"检测到 {len(devices)} 台设备，开始并行处理")
        
        # 创建线程列表
        threads = []
        
        # 为每个设备创建并启动一个线程
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