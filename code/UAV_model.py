import math
import numpy as np

class UAV:
    def __init__(self, name:str,
                initial_position:np.ndarray(shape=(3,), dtype = float),
                communication_range:float):
        """
        初始化无人机的属性。
        """
        # 检查输入参数是否合法
        if initial_position is None:
            raise ValueError("Initial position cannot be None.")
         
        if np.shape(initial_position) != (3,):
            raise ValueError("Initial position must be a 3-array.")
        
        if communication_range <= 0:
            raise ValueError("Communication range must be positive.")

        
        # 初始化无人机的属性
        self.name = name
        self.position = initial_position
        self.communication_range = communication_range
        self.target_detected = None

    def update_position(self, motion_parameters:np.ndarray(shape=(3,), dtype = float)):
        """
        根据速度、飞行间隔和转向角来更新无人机的位置。
        """
        # 检查输入参数是否合法
        if motion_parameters is None:
            raise ValueError("Motion parameters cannot be None.")
        
        if np.shape(motion_parameters) != (3,):
            raise ValueError("Motion parameters must be a 3-array.")
        
        # 局部参数初始化
        x, y, theta = self.position
        velocity, time_interval, turn_angle = motion_parameters

        # 更新航向角,且限制转向角在 [-π, π] 范围内
        if turn_angle <= math.pi and turn_angle >= -math.pi:
            theta += turn_angle
        else:
            # raise ValueError("Turn angle must be in [-π, π].")
            theta += np.sign(turn_angle) * math.pi
        
        # 去除重复周期
        if theta >= 2 * math.pi:
            theta -= 2 * math.pi * (theta % (2 * math.pi))

        # 更新坐标
        x += velocity * math.cos(theta) * time_interval
        y += velocity * math.sin(theta) * time_interval

        self.position = np.array([x, y, theta])

    def detect_target(self, target_position):
        """
        通过检查目标的位置来探测目标。
        """
        distance_to_target = self.calculate_distance(self.position[:2], target_position)
        if distance_to_target <= self.communication_range:
            self.target_detected = target_position
            return True
        else:
            self.target_detected = None
            return False

    def communicate(self, other_uav, message):
        """
        与其他无人机进行通信。
        """
        if self.calculate_distance(self.position[:2], other_uav.position[:2]) <= self.communication_range:
            other_uav.receive_message(message)

    def receive_message(self, message):
        """
        接收来自其他无人机的消息。
        """
        print(f"{self.name} received message: {message}")

    @staticmethod
    def calculate_distance(position1, position2):
        """
        计算两个位置之间的距离。
        """
        x1, y1 = position1
        x2, y2 = position2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 示例用法：
if __name__ == "__main__":
    uav1 = UAV("UAV1", np.array([0, 0, 0]), 5.0)
    uav2 = UAV("UAV2", np.array([2, 3, math.pi/4]), 5.0)
    target_position = (4, 4)

    # 更新无人机位置
    velocity1, time_interval, turn_angle1= 2.0, 1.0, 0.0

    velocity2 = 1.0  # 线速度为1.0
    turn_angle2 = math.pi/6  # 转向角为π/6

    motion_parameters1 = np.array([velocity1, time_interval, turn_angle1])
    uav1.update_position(motion_parameters1)
    
    motion_parameters2 = np.array([velocity2, time_interval, turn_angle2])
    uav2.update_position(motion_parameters2)

    print(uav1.position)
    print(uav2.position)

    # 检测目标
    print(uav1.detect_target(target_position))
    print(uav2.detect_target(target_position))

    # 无人机通信
    uav1.communicate(uav2, "Hello, UAV2!")
