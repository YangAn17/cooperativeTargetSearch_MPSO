# Update the belief map given the current position of UAV and its
# measurement

import numpy as np

# input: 当前更新时刻, 路径长度, 目标运动长度, 目标运动方向, 当前无人机位置, 概率地图
def update_map(current_step, path_length, total_moves, dir, location, map):
    map_size = np.shape(map)
    map_size_x = map_size[0]
    map_size_y = map_size[1]
    
    # Target move direction (totalMoves in the total path)
    move = dir_to_move(dir)
    
    if total_moves != 0:
        move_step = path_length / total_moves   # 栅格运动特点，UAV与目标运动有比例关系
        if current_step % move_step == 0:   # 整数倍关系时需要更新地图
            tmp_map = np.roll(map, move, axis=(0, 1))   # 按照目标运动方向移动地图（目标转移概率地图）
            map = tmp_map / np.sum(tmp_map)    # Scale it to 1
    
    p_sensor_no_detection = np.ones((map_size_x, map_size_y))  # Initialize the probability of no detection with ones
    p_sensor_no_detection[location['y'], location['x']] = 0  # For binary sensor model, the probability of no detection at UAV location is zero
    new_map = p_sensor_no_detection * map  # Update the belief map
    scale_factor = np.sum(new_map)  # Calculate the scaling factor
    new_map = new_map / scale_factor  # Scale the updated belief map
    
    return scale_factor, new_map

# Example usage
if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from DirToMove import dir_to_move

    # 定义模型参数
    current_step = 10
    path_length = 20
    total_moves = 4
    dir = 'E'
    location = {'x': 2, 'y': 2}
    map = np.ones((10, 10))  # 示例地图
    map[5, 5] = 5  # 目标位置
    map = map / np.sum(map)  # 归一化

    # 更新地图
    scale_factor, new_map = update_map(current_step, path_length, total_moves, dir, location, map)
    print("缩放因子:", scale_factor)
    print("更新后的地图:\n", new_map)

    # 可视化地图更新过程
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 创建子图

    # 绘制初始地图
    axes[0].imshow(map, cmap='viridis', origin='lower', vmin=0, vmax=1)
    axes[0].set_title("初始地图")

    # 绘制更新后的地图
    axes[1].imshow(new_map, cmap='viridis', origin='lower', vmin=0, vmax=1)
    axes[1].set_title("更新后的地图")

    plt.tight_layout()
    plt.show()
