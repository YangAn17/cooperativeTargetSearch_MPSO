# Calculate the cost associated to a search path
# Return: costP - The cumulative probability of detection
#

import numpy as np

def my_cost(position, model):
    if not check_motion(position, model):  # Invalid path
        costP = 0  # Punish invalid paths
        return costP
    else:
        # Extract path nodes and convert to map coordinates
        path = path_from_motion(position, model)
        x = path[:, 0]
        y = path[:, 1]

        # Load map and path information/
        Pmap = model['Pmap']  # Input map
        N = model['n']  # path length
        targetMoves = model['targetMoves']  # total moves of the target
        targetDir = model['targetDir']  # target movement direction

        pNodetectionAll = 1  # Initialize the Probability of No detection at all
        pDetection = np.zeros(N)  # Initialize the Probability of detection at each time step

        # Calculate the cost
        for i in range(N):
            location = {'x': x[i] + model['xmax'] + 1, 'y': y[i] + model['ymax'] + 1}  # Shift location to [1, MAPSIZE]
            scaleFactor, Pmap = update_map(i, N, targetMoves, targetDir, location, Pmap)  # Update the probability map

            pNoDetection = scaleFactor  # Probability of No Detection at time t is exactly the scaling factor
            pDetection[i] = pNodetectionAll * (1 - pNoDetection)  # Probability of Detection for the first time at time i
            pNodetectionAll *= pNoDetection

        costP = 1 - pNodetectionAll  # Return the Cumulative Probability of detection up to now (P = 1 - R)
        return costP

# Example usage and testing
if __name__ == "__main__":

    from CheckMotion import check_motion
    from PathFromMotion import path_from_motion
    from UpdateMap import update_map
    from scipy.sparse import rand

    # Define model parameters
    model = {
        'Pmap': np.random.rand(10, 10),  # Example probability map
        'n': 20,
        'xs': 0,
        'ys': 0,
        'xmin': -5,
        'xmax': 5,
        'ymin': -5,
        'ymax': 5,
        'targetMoves': 10,
        'targetDir': 'E'
    }

    # Generate random position
    p = 0.5  # 非零元素的比例
    position = np.random.rand(20, 2)
    position = np.array(position >= p, dtype=int)

    # Calculate cost
    cost = my_cost(position, model)
    print("Cost of the path:", cost)
