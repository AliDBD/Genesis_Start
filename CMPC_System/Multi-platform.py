import os
import time
import subprocess
from api_client import APIClient

class DeviceController:
    def __init__(self):
        self.api_client = APIClient()
        self.device_id = None
    
    def check_device_connection(self):
        """检查设备连接状态"""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = result.stdout.strip().split('\n')[1:]
            if devices and '\tdevice' in devices[0]:
                self.device_id = devices[0].split('\t')[0]
                return True
            return False
        except Exception as e:
            print(f"检查设备连接时出错: {e}")
            return False

    def wake_screen(self):
        """唤醒屏幕"""
        try:
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '26'])
            time.sleep(1)
            return True
        except Exception as e:
            print(f"唤醒屏幕时出错: {e}")
            return False

    def unlock_device(self, password=None):
        """解锁设备"""
        try:
            # 滑动解锁
            subprocess.run(['adb', 'shell', 'input', 'swipe', '300', '1000', '300', '500'])
            
            if password:
                time.sleep(1)
                for digit in password:
                    subprocess.run(['adb', 'shell', 'input', 'text', digit])
                    time.sleep(0.2)
            
            time.sleep(1)
            return True
        except Exception as e:
            print(f"解锁设备时出错: {e}")
            return False

    def check_screen_state(self):
        """检查屏幕状态"""
        try:
            result = subprocess.run(
                ['adb', 'shell', 'dumpsys', 'power'], 
                capture_output=True, 
                text=True
            )
            return 'Display Power: state=ON' in result.stdout
        except Exception as e:
            print(f"检查屏幕状态时出错: {e}")
            return False

    def get_device_info(self):
        """获取设备信息"""
        try:
            model = subprocess.run(
                ['adb', 'shell', 'getprop', 'ro.product.model'],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            android_version = subprocess.run(
                ['adb', 'shell', 'getprop', 'ro.build.version.release'],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            return {
                'model': model,
                'android_version': android_version,
                'device_id': self.device_id
            }
        except Exception as e:
            print(f"获取设备信息时出错: {e}")
            return None

if __name__ == '__main__':
    controller = DeviceController()
    if controller.check_device_connection():
        print("设备已连接")
        device_info = controller.get_device_info()
        print(f"设备信息: {device_info}")
        
        if not controller.check_screen_state():
            controller.wake_screen()
            controller.unlock_device()
    else:
        print("未检测到设备连接")