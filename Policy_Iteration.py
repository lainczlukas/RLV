import numpy as np

from Enums import Actors, Directions
from Environment import Environment

class Policy_Iteration:   
    def __init__(self, environment: Environment):
        self.environment = environment
        self.environment.set_transitions()

        self.grid_size = environment.grid_size
        self.grid_actors = environment.grid_actors

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
                        self.environment.equations['{}{}'.format(x,y)] = []
                        action = self.environment.policy[x,y]
                        equation = "V(s{}{},{}) = ".format(x,y,str(Directions(action).name))
                        state_value = 0

                        for x1 in range(self.grid_size):
                            for y1 in range(self.grid_size):
                                state_value += self.environment.P[x, y, action, x1, y1] * (self.environment.R[x1, y1] + self.gamma * self.environment.V[x1, y1])
                                if self.environment.P[x, y, action, x1, y1] != 0:
                                    equation += "{} * ({} + {}  * {}) + \n".format(round(self.environment.P[x, y, action, x1, y1], 2), self.environment.R[x1, y1], self.gamma, round(self.environment.V[x1, y1], 2))                            
                        self.environment.V[x,y] = state_value
                        equation = equation[:-3]
                        equation += "= {}".format(round(state_value,2))
                        self.environment.equations['{}{}'.format(x,y)].append(equation)

            
            if all(abs(old_values[x,y] - self.environment.V[x,y]) < self.epsilon for x in range(self.grid_size) for y in range(self.grid_size)):
                break


    def policy_improvement(self):
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        equation = "π(s{}{}) = argmax a (\n".format(x,y)
                        Q_values = []
                        for action in range(self.environment.N_actions):
                            q_value = 0
                            for x1 in range(self.grid_size):
                                for y1 in range(self.grid_size):
                                    q_value += self.environment.P[x, y, action, x1, y1] * (self.environment.R[x1, y1] + self.gamma * self.environment.V[x1, y1])
                            
                            equation += "{}, ".format(round(q_value,2))                        
                            Q_values.append(q_value)

                        self.environment.policy[x,y] = np.argmax(Q_values)
                        equation += ") = {}".format(Directions(self.environment.policy[x,y]).name)
                        self.environment.equations['{}{}'.format(x,y)].append(equation)