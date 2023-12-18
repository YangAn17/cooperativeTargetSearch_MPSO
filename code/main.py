import threading
import time
import random
import matplotlib.pyplot as plt
from UAV_model import UAV

# 创建可视化界面
plt.figure(figsize=(8, 6))
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel("X")
plt.ylabel("Y")
plt.ion()  # 开启交互模式

# 绘制目标位置
target_position = (4, 4)
plt.plot(target_position[0], target_position[1], 'ro', label="目标位置")

# 创建无人机
uav1 = UAV("UAV1", (1, 1), 2.0)
uav2 = UAV("UAV2", (3, 2), 2.0)

# 启动无人机搜索任务
threads = []
uav1_thread = threading.Thread(target=uav1.detect_target, args=(target_position,))
uav2_thread = threading.Thread(target=uav2.detect_target, args=(target_position,))
threads.extend([uav1_thread, uav2_thread])
uav1_thread.start()
uav2_thread.start()

while any(thread.is_alive() for thread in threads):
    # 更新图形
    plt.clf()
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.plot(target_position[0], target_position[1], 'ro', label="目标位置")
    for uav in [uav1, uav2]:
        plt.plot(uav.position[0], uav.position[1], 'bo', label=uav.name)
    plt.legend()
    plt.pause(0.1)

# 等待所有无人机完成任务
for thread in threads:
    thread.join()

print("所有无人机已完成任务")
plt.ioff()  # 关闭交互模式
plt.show()
