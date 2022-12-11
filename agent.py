import mesa
import numpy as np

from state import State


class Agent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = State.SUSCEPTIBLE
        self.daysDead = 0
        self.daysExposed = 0
        self.daysInfected = 0
        self.selfQuarantine = False

    def move_to_next(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        
        self.model.grid.move_agent(self, (3,3))

    def infect_others(self, state: State):
        ''' Infect others in same cell based on infection rate '''
        neighbors = self.model.grid.get_cell_list_contents([self.pos])
        if state == State.INFECTED:
            chanceToInfect = self.model.I_E
        elif state == State.DEAD:
            chanceToInfect = self.model.D_E
        else:
            chanceToInfect = 0
        if len(neighbors) > 1:
            for neighbor in neighbors:
                if neighbor.state == State.SUSCEPTIBLE and self.random.random() < chanceToInfect:
                    neighbor.state = State.EXPOSED

    def step(self):
        rand = self.random.random()
        # if not self.selfQuarantine and (
        #         self.state == State.SUSCEPTIBLE or self.state == State.EXPOSED or self.state == State.INFECTED
        # ):
        #     self.move_to_next()
            
        if self.state == State.SUSCEPTIBLE:
            if rand < self.model.S_E:
                self.state = State.EXPOSED
                self.daysExposed = 0
        elif self.state == State.EXPOSED:
            if self.daysExposed < 2:
                pass
            if self.daysExposed > 20:
                self.state = State.INFECTED
                self.selfQuarantine = rand < self.model.Quarantine
            else:
                if rand < self.model.I_E:
                    self.state = State.INFECTED
                    self.selfQuarantine = rand < self.model.Quarantine
                else:
                    self.daysExposed += 1
        elif self.state == State.INFECTED:
            self.infect_others(self.state)
            if rand < self.model.I_R:
                self.state = State.RECOVERED
            elif rand < self.model.I_D + self.model.I_R:
                self.state = State.DEAD
            else:
                if self.daysInfected > self.model.MaxDaysInfected:
                    self.state = State.RECOVERED
                else:
                    self.daysInfected += 1
        elif self.state == State.DEAD:
            self.infect_others(self.state)
            if self.daysDead >= self.model.D_B:
                self.state = State.BURIED
            else:
                self.daysDead += 1
        elif self.state == State.RECOVERED:
            pass
        elif self.state == State.BURIED:
            pass
