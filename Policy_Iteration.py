from msilib.schema import Environment
import numpy as np
from tkinter import Canvas

from Enums import Actors
from Environment import Environment

class Policy_Iteration:   
    def __init__(self, environment: Environment):
        self.environment = environment

        self.grid_size = environment.grid_size
        self.grid_actors = environment.grid_actors

        self.Q = {}

        self.gamma = 0.8
        self.epsilon = 0.5

        self.converged = False


    def step(self, step):
        if self.converged:
            return
        
        for _ in range(step):
            old_policy = self.environment.policy.copy()
            self.policy_evaluation()
            self.policy_improvement()

            self.environment.update_values()
            self.environment.update_policy()

            if all(old_policy[x,y] == self.environment.policy[x,y] for x in range(self.grid_size) for y in range(self.grid_size)):
                self.converged = True
                return


    def policy_evaluation(self):
        self.environment.V = np.zeros((self.grid_size, self.grid_size), float)

        while True:
            old_values = self.environment.V.copy()

            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        action = self.environment.policy[x,y]
                        self.environment.V[x,y] = sum([self.environment.P[x, y, action, x1, y1] * (self.environment.R[x1, y1] + self.gamma * self.environment.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])

            if all(abs(old_values[x,y] - self.environment.V[x,y]) < self.epsilon for x in range(self.grid_size) for y in range(self.grid_size)):
                break


    def policy_improvement(self):
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        Q_values = []
                        for action in range(self.environment.N_actions):
                            Q_values.append(sum(([self.environment.P[x, y, action, x1, y1] * (self.environment.R[x1, y1] + self.gamma * self.environment.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])))
                        
                        self.Q["{}{}".format(x,y)] = Q_values
                        self.environment.policy[x,y] = np.argmax(Q_values)


    def get_Q(self, x, y):
        key = "{}{}".format(x,y)
        if key in self.Q:
            return self.Q[key]
        return [0.0,0.0,0.0,0.0]