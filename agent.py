import mesa
import numpy as np

from state import State


class Agent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = State.SUSCEPTIBLE
        self.daysDead = 0

    def move_to_next(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect_others(self):
        ''' Infect others in same cell based on infection rate '''
        neighbors = self.model.grid.get_cell_list_contents([self.pos])
        if len(neighbors) > 1:
            for neighbor in neighbors:
                if neighbor.state == State.EXPOSED and self.random.random() < self.model.E_I:
                    neighbor.state = State.INFECTED

    def step(self):
        rand = self.random.random()
        if rand < self.model.P and (
                self.state == State.SUSCEPTIBLE or self.state == State.EXPOSED or self.state == State.INFECTED
        ):
            self.move_to_next()

        if self.state == State.SUSCEPTIBLE:
            if rand < self.model.S_E:
                self.state = State.EXPOSED
        elif self.state == State.EXPOSED:
            if rand < self.model.E_I:
                self.state = State.INFECTED
        elif self.state == State.INFECTED:
            self.infect_others()
            if self.random.random() < 0.5:
                if rand < self.model.I_R:
                    self.state = State.RECOVERED
            else:
                if rand < self.model.I_D:
                    self.state = State.DEAD
        elif self.state == State.DEAD:
            if self.daysDead >= self.model.D_B:
                self.state = State.BURIED
            else:
                self.daysDead += 1
        elif self.state == State.RECOVERED:
            pass
        elif self.state == State.BURIED:
            pass
