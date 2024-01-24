import numpy as np
from scipy.stats import multivariate_normal

def create_model():
    # Create a grid map
    MAP_SIZE = 40
    x = np.arange(1, MAP_SIZE + 1)
    y = np.arange(1, MAP_SIZE + 1)
    X, Y = np.meshgrid(x, y)    # X row vectors are the same, Y column vectors are the same

    # Generate the probability map
    mu1 = np.array([10, 10])    # mean vector
    Sigma1 = MAP_SIZE * np.array([[0.1, 0], [0, 0.1]])  # covariance matrix
    coords = np.column_stack((X.flatten(), Y.flatten()))    # matrix X and Y are flattened and stacked together
    F1 = multivariate_normal.pdf(coords, mean=mu1, cov=Sigma1)  # create a probability distribution
    F1 = np.reshape(F1, (len(y), len(x)))   # reshape the distribution to the size of the map
    F1 = F1 / np.sum(F1)    # normalize the distribution

    mu2 = np.array([5, 5])
    Sigma2 = MAP_SIZE * np.array([[0.1, 0], [0, 0.1]])
    F2 = multivariate_normal.pdf(coords, mean=mu2, cov=Sigma2)
    F2 = np.reshape(F2, (len(y), len(x)))
    F2 = F2 / np.sum(F2)

    Pmap = 0.5 * (F1 + F2)  # normalize the probability map

    # Settings
    xmin = -MAP_SIZE // 2
    xmax = MAP_SIZE // 2
    ymin = -MAP_SIZE // 2
    ymax = MAP_SIZE // 2
    xs = 0  # Start search X position
    ys = 0  # Start search Y position
    n = 20
    MRANGE = 4

    # Model
    model = {
        'xs': xs,
        'ys': ys,
        'Pmap': Pmap,
        'n': n,
        'xmin': xmin,
        'xmax': xmax,
        'ymin': ymin,
        'ymax': ymax,
        'MRANGE': MRANGE,
        'MAPSIZE': MAP_SIZE,
        'X': X,
        'Y': Y,
        'targetMoves': 10,  # Must be divisible by the path length (e.g, mod(N,move)=0)
        'targetDir': 'E'    # The target moves direction
    }

    return model

# Example usage
if __name__ == '__main__':
    model_instance = create_model()
    print(model_instance)
