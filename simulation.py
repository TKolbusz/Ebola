from mesa import Model
from mesa.time import RandomActivation
from agent import Agent
from mesa.space import MultiGrid
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from state import State


def total_infected(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.state == State.INFECTED:
            total += 1
    return total


def total_dead(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.state == State.DEAD or agent.state == State.BURIED:
            total += 1
    return total


def total_recovered(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.state == State.RECOVERED:
            total += 1
    return total


class Simulation(Model):
    """A model with some number of agents."""

    def __init__(self, params, seed=None):
        self.N = params.get('N')
        self.K = params.get('K')
        self.P = params.get('P')

        
        # self.grid = MultiGrid(params.get('x'), params.get('y'), True)
        self.G = nx.watts_strogatz_graph(n=self.N, k=self.K, p=self.P)
        self.grid = NetworkGrid(self.G)


        self.schedule = RandomActivation(self)

        
        self.S_E = params.get('S_E')
        self.I_E = params.get('I_E')
        self.Q_I_E = params.get('Q_I_E')
        self.Q = params.get('Q')
        self.D_E = params.get('D_E')
        self.I_D = params.get('I_D')
        self.I_R = params.get('I_R')
        self.MaxDaysInfected = params.get('MaxDaysInfected')
        self.MaxDaysExposed = params.get('MaxDaysExposed')
        self.D_B = params.get('D_B')

        self.running = True
        self.cycle = 0

        for i, node in enumerate(self.G.nodes()):
            a = Agent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, node)

        # for i in range(self.N):
        #     a = Agent(i, self)
        #     self.schedule.add(a)
        #     # place Agent randomly on the grid
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={
                "Infected": total_infected,
                "Deaths": total_dead,
                "Recovered": total_recovered
            })

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()
        self.cycle += 1
