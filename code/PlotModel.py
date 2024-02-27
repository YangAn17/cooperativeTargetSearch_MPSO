# Plot the search map

import numpy as np
import matplotlib.pyplot as plt

def plot_model(model):
    MAP_SIZE = model['MAPSIZE']
    x = np.arange(1, MAP_SIZE + 1)
    y = np.arange(1, MAP_SIZE + 1)
    X, Y = np.meshgrid(x, y)
    
    plt.clf()
    h = plt.pcolormesh(X, Y, model['Pmap'])
    
    # Start position
    plt.plot(model['xs'] + MAP_SIZE // 2 + 0.5, model['ys'] + MAP_SIZE // 2 + 0.5, 'wo', markersize=3, markerfacecolor='w', linewidth=1)
    
    plt.xlabel('x (cell)')
    plt.ylabel('y (cell)')
    
    # Set properties
    h.set_linewidth(0.1)
    cb = plt.colorbar(h)
    cb.formatter.set_powerlimits((-3, -3))
    cb.update_ticks()
    gcaP = plt.gca().get_position()
    cbP = cb.ax.get_position()
    cbP = (cbP.x0, cbP.y0, cbP.width / 2, cbP.height)  # Change the colorbar width
    cb.ax.set_position(cbP)
    plt.gca().set_position(gcaP)
    plt.gcf().set_size_inches(3.5, 2.5)  # Set the map size
    plt.show()

# Example usage
if __name__ == "__main__":
    model = {
        'MAPSIZE': 40,
        'Pmap': np.random.rand(40, 40),
        'xs': 0,
        'ys': 0
    }
    plot_model(model)
