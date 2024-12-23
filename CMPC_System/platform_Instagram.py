#!/usr/bin/env python
# -- coding: utf-8 --
import subprocess
import time
import logging
import sys
import random
import threading  # 添加到文件开头的导入部分

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
        
        # 等待应用完全加载
        time.sleep(5)
        
        # 这里添加您需要的具体操作
        # 例如：点击底部导航栏的"搜索"按钮
        tap_point(udid, 360, 1280)  # 这里的坐标需要根据实际设备调整
        time.sleep(2)
        
        # 点击搜索框
        tap_point(udid, 540, 144)  # 这里的坐标需要根据实际设备调整
        time.sleep(2)
        
        # 可以继续添加更多操作...
        
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