from Enums import Actors, Directions
from Environment import Environment

import numpy as np

from random import uniform, choice


class Sarsa:
    def __init__(self, environment: Environment):
        self.environment = environment
        self.environment.set_transitions()

        self.grid_size = environment.grid_size
        self.space_width = self.environment.space_width
        self.space_height = self.space_width
        self.qtable = np.zeros((self.grid_size, self.grid_size, 4))

        self.gamma = 0.8
        self.learning_rate = 0.2
        self.epsilon = 0.15

        self.start = np.where(environment.grid_actors == Actors.agent)
        self.current_state = (int(self.start[0]), int(self.start[1]))
        self.converged = False

        self.environment.draw_policy()
        self.environment.init_equation()


    def step(self, step):
        if self.converged:
            return
            

        for _ in range(step):
            done = False
            
            if uniform(0, 1) > self.epsilon:
                action = np.argmax(self.qtable[self.current_state[0], self.current_state[1]])
            else:
                action = choice([0,1,2,3])

            next_state, reward, done = self.environment.get_new_state(action, self.current_state)

            self.environment.equations['{}{}'.format(self.current_state[0], self.current_state[1])] = []
            equation = "Q({},{}) = [".format(self.current_state[0], self.current_state[1])
            for i in range(4):
                equation += "{}={},".format(Directions(i).name ,round(self.qtable[self.current_state[0], self.current_state[1], i], 2))
            equation = equation[:-1] + ']'
            self.environment.equations['{}{}'.format(self.current_state[0], self.current_state[1])].append(equation)

            new_Q =  self.qtable[self.current_state[0], self.current_state[1], action] + self.learning_rate * (reward + self.gamma * self.qtable[next_state[0], next_state[1], np.argmax(self.qtable[next_state[0], next_state[1]])] - self.qtable[self.current_state[0], self.current_state[1], action])
            equation = "Q({},{}|{}) = {} + {}*({}+{}*{} - {}) \n= {}".format(self.current_state[0], self.current_state[1], Directions(action).name, round(self.qtable[self.current_state[0], self.current_state[1], action],2), self.learning_rate, reward, self.gamma, round(self.qtable[next_state[0], next_state[1], np.argmax(self.qtable[next_state[0], next_state[1]])],2), round(self.qtable[self.current_state[0], self.current_state[1], action],2), round(new_Q,2))
            self.environment.equations['{}{}'.format(self.current_state[0], self.current_state[1])].append(equation)

            self.qtable[self.current_state[0], self.current_state[1], action] = new_Q

            self.environment.policy[self.current_state[0], self.current_state[1]] = np.argmax(self.qtable[self.current_state[0], self.current_state[1], :])
            self.environment.update_policy_on(self.current_state[0], self.current_state[1])

            self.environment.V[self.current_state[0], self.current_state[1]] = max(self.qtable[self.current_state[0], self.current_state[1], :])
            self.environment.update_values_on(self.current_state[0], self.current_state[1])

            equation = "Q({},{}) = [".format(self.current_state[0], self.current_state[1])
            for i in range(4):
                equation += "{}={},".format(Directions(i).name ,round(self.qtable[self.current_state[0], self.current_state[1], i], 2))
            equation = equation[:-1] + ']'
            self.environment.equations['{}{}'.format(self.current_state[0], self.current_state[1])].append(equation)

            if done:
                self.current_state = (int(self.start[0]), int(self.start[1]))
                self.environment.draw_agent(self.current_state)
            else:
                self.environment.draw_agent(next_state)
                self.current_state = next_state