from mesa import Model
from mesa.time import RandomActivation
from agent import Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import matplotlib.pyplot as plt

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
        self.grid = MultiGrid(params.get('x'), params.get('y'), True)
        self.schedule = RandomActivation(self)

        self.S_E = params.get('S_E')
        self.I_E = params.get('I_E')
        self.D_E = params.get('D_E')
        self.I_D = params.get('I_D')
        self.I_R = params.get('I_R')
        self.Quarantine = params.get('Quarantine')
        self.MaxDaysInfected = params.get('MaxDaysInfected')
        self.D_B = params.get('D_B')

        self.running = True
        self.cycle = 0

        for i in range(self.N):
            a = Agent(i, self)
            self.schedule.add(a)
            # place Agent randomly on the grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

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
