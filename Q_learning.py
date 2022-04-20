from Enums import Actors, Directions
from Environment import Environment

import numpy as np

from random import uniform, choice


class Q_learning:
    def __init__(self, environment: Environment):
        self.environment = environment

        self.grid_size = environment.grid_size
        self.grid_actors = environment.grid_actors

        self.space_width = self.environment.space_width
        self.space_height = self.space_width
        self.qtable = np.zeros((self.grid_size, self.grid_size, 4))

        self.gamma = 0.8
        self.learning_rate = 0.8
        self.epsilon = 0.2

        self.start = np.where(environment.grid_actors == Actors.agent)

        self.current_state = (self.start[0], self.start[1])

        self.converged = False


    def step(self, step):
        if self.converged:
            return
            

        for _ in range(step):
            done = False
            self.current_state = (self.start[0], self.start[1])

            while done == False:
                if uniform(0, 1) > self.epsilon:
                    action = np.argmax(self.qtable[self.current_state[0], self.current_state[1]])
                else:
                    action = choice([0,1,2,3])

                next_state, reward, done = self.get_new_state(action)

                self.qtable[self.current_state[0], self.current_state[1], action] =  self.qtable[self.current_state[0], self.current_state[1], action] + self.learning_rate * (reward + self.gamma * self.qtable[next_state[0], next_state[1], action] - self.qtable[self.current_state[0], self.current_state[1], action])

                self.current_state = next_state

    def get_new_state(self, action):
        weights = self.environment.P[self.current_state[0], self.current_state[1], action]
        next_state = np.random.choice((), p=weights)
        print(action)
        print(next_state)