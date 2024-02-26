# Create a search path from the encoded motions
#

import numpy as np

def path_from_motion(position, model):
    n = model['n']
    xs = model['xs']
    ys = model['ys']
    path = np.zeros((n, 2))  # path initialisation
    current_node = np.array([xs, ys])
    for i in range(n):
        motion = position[i, :]
        next_move = motion_decode(motion)
        next_node = current_node + next_move

        # Limit the path to be within the map
        # x direction
        if next_node[0] > model['xmax']:
            next_node[0] = model['xmax']
        elif next_node[0] < model['xmin']:
            next_node[0] = model['xmin']
        # y direction
        if next_node[1] > model['ymax']:
            next_node[1] = model['ymax']
        elif next_node[1] < model['ymin']:
            next_node[1] = model['ymin']
        
        path[i, :] = current_node
        current_node = next_node

    return path

# Example usage
if __name__ == "__main__":

    from MotionDecode import motion_decode

    model = {
        'n': 4,
        'xs': 0,
        'ys': 0,
        'xmin': -10,
        'xmax': 10,
        'ymin': -10,
        'ymax': 10
    }
    position = np.array([[1, 0], [1, 0], [0, 1], [0, 1]])

    print("Search path from encoded motions:")
    print(path_from_motion(position, model))
