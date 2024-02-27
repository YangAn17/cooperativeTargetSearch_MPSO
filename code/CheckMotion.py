# Check if the encoded motion forms a valid path
#

import numpy as np
from MotionDecode import motion_decode

def check_motion(position, model):
    # Load model parameters
    n = model['n']
    xs = model['xs']
    ys = model['ys']
    path = np.zeros((n, 2))  # The path consists of n nodes, each node is (x,y)
    current_node = np.array([xs, ys])
    valid = True
    
    # Decode from the motions to a path
    for i in range(n):
        motion = position[i]
        next_move = motion_decode(motion)  
        next_node = current_node + next_move
        
        # Out of map boundary
        if (next_node[0] > model['xmax'] or next_node[0] < model['xmin'] or
            next_node[1] > model['ymax'] or next_node[1] < model['ymin']):
            valid = False
            return valid
            
        path[i] = next_node
        current_node = next_node
    
    # Check duplicate rows
    _, indices = np.unique(path, axis=0, return_index=True)
    print("Unique indices:", indices)
    if len(indices) < n:
        valid = False
    return valid

# Example usage
if __name__ == "__main__":

    from MotionDecode import motion_decode

    model = {
        'n': 4,
        'xs': 0,
        'ys': 0,
        'xmin': -2,
        'xmax': 2,
        'ymin': -2,
        'ymax': 2
    }
    position_valid = np.array([[1, 0], [1, 0], [0, 1], [0, 1]])
    position_invalid1 = np.array([[1, 0], [1, 0], [0, 1], [1, 0]])
    position_invalid2 = np.array([[1, 0], [0, 1], [-0.7071, -0.7071], [1, 0]])

    print("Testing valid motion:")
    print(check_motion(position_valid, model))  # Should print True

    print("Testing invalid motion (out boundary node):")
    print(check_motion(position_invalid1, model))  # Should print False

    print("Testing invalid motion (duplicated node):")
    print(check_motion(position_invalid2, model))  # Should print False
