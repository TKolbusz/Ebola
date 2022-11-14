from enum import Enum


class State(Enum):
    SUSCEPTIBLE = 1
    EXPOSED = 2
    INFECTED = 3
    RECOVERED = 4
    DEAD = 5
    BURIED = 6
