from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules.HexGridVisualization import CanvasHexGrid
from mesa.visualization.modules.NetworkVisualization import NetworkModule

from simulation import Simulation, total_dead, total_recovered
from state import State

params = {
    "N": 100, # number of Agents
    "x": 100,
    "y": 100,
    "S_E": 0.05,  # possibility of becoming exposed by itself
    "I_E": 0.25,  # possibility infecting while being infected
    "D_E": 0.1,  # possibility infecting while being dead
    "I_D": 0.10,  # possibility of Infected -> Dead transition
    "I_R": 0.04,  # possibility of Infected -> Recovered transition
    "MaxDaysInfected" : 7,
    "MaxDaysExposed" : 20,
    "D_B": 3,  # days it takes to bury the dead
}



def agent_portrayal(G):
    def node_color(agent):
        return {
            State.INFECTED: '#c1023b',
            State.EXPOSED: '#ff461f',
            State.RECOVERED: '#1aa478',
            State.DEAD: "#000000",
            State.BURIED: "#511111"
        }.get(agent.state, '#e1e1e1')

    def edge_color(agent1, agent2):
        if (State.INFECTED == agent1.state and State.SUSCEPTIBLE == agent2.state) or (State.INFECTED == agent2.state and State.SUSCEPTIBLE == agent1.state):
            return "#c1023b"
        
        return "#e1e1e1"

    def get_agents(source, target):
        return G.nodes[source]['agent'][0], G.nodes[target]['agent'][0]

    portrayal = dict()
    portrayal['nodes'] = [{'size': 6,
                           'color': node_color(agents[0]),
                           'tooltip': "id: {}<br>state: {}".format(agents[0].unique_id, agents[0].state.name),
                           }
                          for (_, agents) in G.nodes.data('agent')]

    portrayal['edges'] = [{'source': source,
                           'target': target,
                           'color': edge_color(*get_agents(source, target)),
                           'width': 3,
                           }
                          for (source, target) in G.edges]

    return portrayal


# grid = CanvasGrid(
#     agent_portrayal,
#     params.get('x'),
#     params.get('y'),
#     params.get('x') * 16,
#     params.get('y') * 16)

# networkGrid = NetworkModule(
#     agent_portrayal,
#     700,
#     700
# )



# test each value 100 times
runsPerParameterValue=100
# testing certain parameter
x=[]
y=[]
for i in range(0,31):
    # modify some parameter in a loop

    # check bury time in days
    params["D_B"] = i
    # check max infected time
    # params["MaxDaysInfected"] = i
    # params["MaxDaysExposed"] = i

    sim = Simulation(params)
    agentCount = params.get("N")
    runs = []
    for j in range(0,runsPerParameterValue):
        # prevent never ending loop
        maxLoops = 100000
        while (total_dead(sim) + total_recovered(sim)) < agentCount and maxLoops > 0:
            sim.step()
            maxLoops = maxLoops-1
        deadCount = total_dead(sim)
        recoveredCount = total_recovered(sim)
        death_rate = deadCount/agentCount
        runs.append(death_rate)
    avg = mean(runs)
    x.append(i)
    y.append(avg)

coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef)
plt.plot(x,y,'ro',x,poly1d_fn(x),'--k')

plt.xlabel('Bury time in days')
plt.ylabel('Death rate')

plt.title('How does bury time(in days) affect the death rate?')

plt.show()


# chart = ChartModule([{"Label": "Infected",
#                       "Color": "Red"},
#                      {"Label": "Recovered",
#                       "Color": "Green"},
#                      {"Label": "Deaths",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')
# server = ModularServer(Simulation,
#                        [networkGrid, chart],
#                        "Ebola Model",
#                        {"params": params})
# server.port = 8521
# server.launch()
