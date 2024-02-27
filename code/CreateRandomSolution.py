#Create random paths (solutions)
#

import numpy as np
from MotionDecode import motion_decode

def create_random_solution(model):
    n = model['n']  # Load the number of path nodes
    start_node = np.array([model['xs'], model['ys']])
    path = np.zeros((n, 2))  # path initialization
    max_it = 100  # Maximum number of trial iterations before resetting the path

    motions = np.array([[1, 0],
                        [0.7071, 0.7071],
                        [0, 1],
                        [-0.7071, 0.7071],
                        [-1, 0],
                        [-0.7071, -0.7071],
                        [0, -1],
                        [0.7071, -0.7071]])

    should_restart = True

    # Repeat until generating a valid path
    while should_restart:
        should_restart = False
        path = np.tile(start_node, (n, 1))  # np.tile(A, reps)结果为重复A为reps(分行列)次
        position = np.zeros((n, 2))  # motion initialisation
        current_node = start_node
        for i in range(n):
            motion = motions[np.random.randint(0, len(motions)), :]
            invalid_flag = True
            it = 0
            while invalid_flag and it < max_it:
                next_move = motion_decode(motion)
                next_node = current_node + next_move
                invalid_flag = False

                # Limit the path to be within the map
                # Out of x direction -> Move it back
                if next_node[0] > model['xmax']:
                    motion = motions[4, :]  # Move it [-1, 0] to back
                    invalid_flag = True
                    it += 1
                elif next_node[0] < model['xmin']:
                    motion = motions[0, :]  # Move it [1, 0] to back
                    invalid_flag = True
                    it += 1

                # Out of y direction
                elif next_node[1] > model['ymax']:
                    motion = motions[6, :]
                    invalid_flag = True
                    it += 1
                elif next_node[1] < model['ymin']:
                    motion = motions[2, :]
                    invalid_flag = True
                    it += 1
                else:
                    # Check duplicate nodes within a path
                    for j in range(len(path)):
                        if np.array_equal(next_node, path[j, :]):   # 判断两个数组是否相等
                            motion = motions[np.random.randint(0, len(motions)), :]
                            invalid_flag = True
                            it += 1
                            break

            # Restart the whole path
            if it >= max_it:
                should_restart = True
                break
            else:  # Path ok
                path[i, :] = next_node
                current_node = next_node
                position[i, :] = motion

    return position

# Example usage
if __name__ == "__main__":
    
    from MotionDecode import motion_decode

    model = {
        'n': 4,
        'xs': 0,
        'ys': 0,
        'xmin': -20,
        'xmax': 20,
        'ymin': -20,
        'ymax': 20
    }

    print("Random solution:")
    print(create_random_solution(model))
