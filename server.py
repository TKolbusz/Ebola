from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from simulation import Simulation
from state import State

params = {
    "N": 100,
    "x": 100,
    "y": 100,
    "S_E": 0.05,  # possibility of Susceptible -> Exposed transition
    "E_I": 0.06,  # possibility of Exposed -> Infected transition
    "I_D": 0.07,  # possibility of Infected -> Dead transition
    "I_R": 0.10,  # possibility of Infected -> Recovered transition
    "P": 0.50,  # probability od Edge moving - not used ATM
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
