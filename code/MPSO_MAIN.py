import numpy as np
from CreateModel import create_model
from MyCost import my_cost
from PathFromMotion import path_from_motion
from PlotSolution import plot_solution
from CreateRandomSolution import create_random_solution
from DirToMove import dir_to_move
from noncircshift import noncircshift

# Assume CreateModel, MyCost, PathFromMotion, PlotSolution are defined in other files

def main():
    # CreateModel() function is assumed to be defined elsewhere
    model = create_model()  # Create search map and parameters

    CostFunction = lambda x: my_cost(x, model)  # Cost Function

    nVar = model['n']  # Number of Decision Variables = searching dimension of PSO = number of movements

    VarSize = (nVar, 2)  # Size of Decision Variables Matrix

    VarMin = -model['MRANGE']  # Lower Bound of particles (Variables)
    VarMax = model['MRANGE']  # Upper Bound of particles

    # PSO Parameters
    MaxIt = 100  # Maximum Number of Iterations
    nPop = 1000  # Population Size (Swarm Size)
    w = 1  # Inertia Weight
    wdamp = 0.98  # Inertia Weight Damping Ratio
    c1 = 2.5  # Personal Learning Coefficient
    c2 = 2.5  # Global Learning Coefficient
    alpha = 2
    VelMax = alpha * (VarMax - VarMin)  # Maximum Velocity
    VelMin = -VelMax  # Minimum Velocity

    # Initialization
    empty_particle = {'Position': None, 'Velocity': None, 'Cost': None, 'Best': {'Position': None, 'Cost': None}}
    GlobalBest = {'Cost': -1}  # Maximization problem
    particles = [empty_particle.copy() for _ in range(nPop)]

    # Initialization Loop
    for i in range(nPop):
        # Initialize Position
        particles[i]['Position'] = create_random_solution(model)
        # Initialize Velocity
        particles[i]['Velocity'] = np.zeros(VarSize)
        # Evaluation
        costP = CostFunction(particles[i]['Position'])
        particles[i]['Cost'] = costP
        # Update Personal Best
        particles[i]['Best']['Position'] = particles[i]['Position']
        particles[i]['Best']['Cost'] = particles[i]['Cost']
        # Update Global Best
        if particles[i]['Best']['Cost'] > GlobalBest['Cost']:
            GlobalBest = particles[i]['Best'].copy()

    # Array to Hold Best Cost Values at Each Iteration
    BestCost = np.zeros(MaxIt)

    # PSO Main Loop
    for it in range(MaxIt):
        for i in range(nPop):
            # Update Velocity
            particles[i]['Velocity'] = w * particles[i]['Velocity'] \
                + c1 * np.random.rand(*VarSize) * (particles[i]['Best']['Position'] - particles[i]['Position']) \
                + c2 * np.random.rand(*VarSize) * (GlobalBest['Position'] - particles[i]['Position'])
            # Update Velocity Bounds
            particles[i]['Velocity'] = np.maximum(particles[i]['Velocity'], VelMin)
            particles[i]['Velocity'] = np.minimum(particles[i]['Velocity'], VelMax)
            # Update Position
            particles[i]['Position'] = particles[i]['Position'] + particles[i]['Velocity']
            # Update Position Bounds
            particles[i]['Position'] = np.maximum(particles[i]['Position'], VarMin)
            particles[i]['Position'] = np.minimum(particles[i]['Position'], VarMax)
            # Evaluation
            costP = CostFunction(particles[i]['Position'])
            particles[i]['Cost'] = costP
            # Update Personal Best
            if particles[i]['Cost'] > particles[i]['Best']['Cost']:
                particles[i]['Best']['Position'] = particles[i]['Position']
                particles[i]['Best']['Cost'] = particles[i]['Cost']
                # Update Global Best
                if particles[i]['Best']['Cost'] > GlobalBest['Cost']:
                    GlobalBest = particles[i]['Best'].copy()

        # Update Best Cost Ever Found
        BestCost[it] = GlobalBest['Cost']
        # Inertia Weight Damping
        w = w * wdamp

        # Show Iteration Information
        print('Iteration {}: Best Cost = {}'.format(it + 1, BestCost[it]))

    # Results
    # Updade Map in Accordance to the Target Moves
    targetMoves = model['targetMoves']  # Number of Target Moves (Zero means static)
    moveDir = dir_to_move(model['targetDir'])  # Direction of the Target Movement
    moveArr = targetMoves * moveDir
    updatedMap, _, __ = noncircshift(model['Pmap'], moveArr)
    newModel = model
    newModel['Pmap'] = updatedMap

    # Plot Solution
    # PathFromMotion and PlotSolution functions are assumed to be defined elsewhere
    path = path_from_motion(GlobalBest['Position'], model)  # Convert from Motion to Cartesian Space
    plot_solution(path, newModel)

    # Plot Best Cost Over Iterations
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(BestCost, linewidth=2)
    plt.xlabel('Iteration')
    plt.ylabel('Best Cost')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
