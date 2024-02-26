# Convert the encoded motion from an array of 8 numbers to a move
# Eight numbers encode the magnitude of a vector with the angle of
# NW, N, NE, W, E, SW, S, SE
# 1   2   3  4  5   6  7  8
#

import numpy as np

def motion_decode(motion):
    # Find the angle of the sum vector
    angle = np.arctan2(motion[1], motion[0])

    # Map the angle to its corresponding octant (0, 45, 90, 135 ...)
    octant = (round(8 * angle / (2 * np.pi) + 8) % 8) + 1

    move_array = np.array(
        [[1, 0],
        [1, 1],
        [0, 1],
        [-1, 1],
        [-1, 0],
        [-1, -1],
        [0, -1],
        [1, -1]])

    # Map the octant to a move
    move = move_array[octant - 1]

    return move

# Example usage
if __name__ == "__main__":
    motion_vector = [1, 0]
    decoded_direction = motion_decode(motion_vector)
    print(decoded_direction)
