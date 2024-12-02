import numpy as np
import matplotlib.pyplot as plt

# 定义重力加速度（m/s^2）
g = 9.8

# 定义时间数组，从0到10秒，步长为0.1秒
t = np.arange(0, 10, 0.1)

# 计算位置和速度
s = 0.5 * g * t**2
v = g * t

# 创建一个图形对象
plt.figure(figsize=(10, 5))

# 绘制位置-时间图像
plt.subplot(1, 2, 1)
plt.plot(t, s, label='Position (s)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Position vs Time')
plt.legend()

# 绘制速度-时间图像
plt.subplot(1, 2, 2)
plt.plot(t, v, label='Velocity (v)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs Time')
plt.legend()

# 显示图像
plt.tight_layout()
plt.show()
