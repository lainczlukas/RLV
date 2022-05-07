from Enums import Actors, Directions
from Environment import Environment

class Value_Iteration:   
    def __init__(self, environment: Environment):
        self.environment = environment

        self.grid_size = environment.grid_size
        self.grid_actors = environment.grid_actors

        self.space_width = self.environment.space_width
        self.space_height = self.space_width

        self.gamma = 0.8
        self.theta = 0.5

        self.converged = False


    def step(self, step):
        if self.converged:
            return
            
        delta = self.theta + 1.0

        for _ in range(step):
            delta = 0.0
            
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        prev_value = self.environment.V[x,y]
                        action_values = []
                        self.environment.equations['{}{}'.format(x,y)] = []
                        
                        for action in range(self.environment.N_actions):
                            equation = "V(s{}{},{}) = ".format(x,y,str(Directions(action).name))
                            action_value = 0

                            for x1 in range(self.grid_size):
                                for y1 in range(self.grid_size):
                                    action_value += self.environment.P[x, y, action, x1, y1] * (self.environment.R[x1, y1] + self.gamma * self.environment.V[x1, y1])
                                    if self.environment.P[x, y, action, x1, y1] != 0:
                                        equation += "{} * ({} + {}  * {}) + \n".format(round(self.environment.P[x, y, action, x1, y1], 2), self.environment.R[x1, y1], self.gamma, round(self.environment.V[x1, y1], 2))                            

                            action_value = round(action_value, 2) 
                            action_values.append(action_value)
                            equation = equation[:-3]
                            equation += "= {}".format(action_value)
                            self.environment.equations['{}{}'.format(x,y)].append(equation)

                        self.environment.V[x, y] = max(action_values)
                        delta = max(delta, abs(prev_value - self.environment.V[x, y]))
            
            if delta < self.theta:
                self.environment.update_values()
                self.calculate_policy()
                self.converged = True
                return
        
        self.environment.update_values()    


    def calculate_policy(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle and self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                    best_action = 11.0
                    for action in range(self.environment.N_actions):
                        action_value = sum([self.environment.P[x, y, action, x1, y1] * (self.environment.R[x1, y1] + self.gamma * self.environment.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])
                        if best_action == 11.0 or action_value > best_action:
                            best_action = action_value
                            self.environment.policy[x,y] = action
        
        self.environment.draw_policy()