from enum import Enum

class Actors(Enum):
    empty = 0
    agent = 1
    goal = 2
    monster = 3
    obstacle = 4

class Directions(Enum):
    N = 0
    E = 1
    S = 2
    W = 3