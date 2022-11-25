from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from simulation import Simulation
from state import State

params = {
    "N": 200, # number of Agents
    "x": 100,
    "y": 100,
    "S_E": 0.01,  # possibility of becoming exposed by itself
    "I_E": 0.4,  # possibility infecting while being infected
    "D_E": 0.1,  # possibility infecting while being dead
    "I_D": 0.15,  # possibility of Infected -> Dead transition
    "I_R": 0.07,  # possibility of Infected -> Recovered transition
    "Quarantine" : 0.5,
    "MaxDaysInfected" : 7,
    "D_B": 3,  # days it takes to bury the dead
}


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.8}

    if agent.state == State.INFECTED:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        if agent.state == State.RECOVERED:
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0

    if agent.state == State.DEAD or agent.state == State.BURIED:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0

    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    params.get('x'),
    params.get('y'),
    params.get('x') * 4,
    params.get('y') * 4)
chart = ChartModule([{"Label": "Infected",
                      "Color": "Red"},
                     {"Label": "Recovered",
                      "Color": "Green"},
                     {"Label": "Deaths",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
server = ModularServer(Simulation,
                       [grid, chart],
                       "Ebola Model",
                       {"params": params})
server.port = 8521
server.launch()
