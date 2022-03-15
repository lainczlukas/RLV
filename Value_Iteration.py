import numpy as np
from tkinter import Canvas

from Enums import Actors

class Value_Iteration:   
    def __init__(self, grid_size, grid_actors, canvas_grid: Canvas, space_width, space_height, stochastic):
        self.grid_size = grid_size
        self.grid_actors = grid_actors
        self.canvas_grid = canvas_grid
        self.space_width = space_width
        self.space_height = space_height
        self.stochastic = stochastic
        
        self.R = np.full((self.grid_size, self.grid_size), -1.0)
        self.V = np.zeros((self.grid_size, self.grid_size), float)
        self.draw_rewards()
        self.draw_values()

        self.A = [0, 1, 2, 3]
        self.N_actions = len(self.A)

        self.set_transitions()

        self.gamma = 0.8
        self.theta = 0.5


    def step(self, step):
        delta = self.theta + 1.0

        for _ in range(step):
            delta = 0.0
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        prev_value = self.V[x,y]
                        action_values = list()
                        for action in range(self.N_actions):
                            action_value = sum([self.P[x, y, action, x1, y1] * (self.R[x1, y1] + self.gamma * self.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])
                            action_values.append(action_value)                   
                        self.V[x, y] = max(action_values)
                        delta = max(delta, abs(prev_value - self.V[x, y]))
            
            if delta < self.theta:
                self.update_values()
                self.calculate_policy()
                return
        
        self.update_values()


    def calculate_policy(self):
        policy = np.full((self.grid_size, self.grid_size),-1 ,dtype=float)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle and self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                    best_action = 11.0
                    for action in range(self.N_actions):
                        action_value = sum([self.P[x, y, action, x1, y1] * (self.R[x1, y1] + self.gamma * self.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])
                        if best_action == 11.0 or action_value > best_action:
                            best_action = action_value
                            policy[x,y] = action
        
        direction = {0: "N", 1: "E", 2: "S", 3:"W"}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster and self.grid_actors[x,y] != Actors.obstacle:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 1.4, 
                        y * self.space_height + self.space_height / 1.4, 
                        text=direction[policy[x,y]], 
                        fill = "#000", 
                        font = ("RobotoRoman-Bold", int(self.space_width / 7)),
                        tags='V{}{}'.format(x,y))


    def update_values(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle:
                    text = self.canvas_grid.find_withtag('V{}{}'.format(x,y))
                    self.canvas_grid.itemconfig(text, text=str(round(self.V[x,y], 2)))


    def set_transitions(self):
        self.P = np.zeros((self.grid_size, self.grid_size, self.N_actions, self.grid_size, self.grid_size))
        fraction = 0.1

        if (self.stochastic == 1):
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    #North
                    counter = 0.0
                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                            self.P[x, y, 0, x, y+1] = fraction
                            counter += fraction
                        if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                            self.P[x, y, 0, x+1, y] = fraction
                            counter += fraction
                        if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                            self.P[x, y, 0, x-1, y] = fraction
                            counter += fraction
                        self.P[x, y, 0, x, y-1] = 1.0 - counter
                    else:
                        self.P[x, y, 0, x, y] = 1.0
                    
                    #East
                    counter = 0.0
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                            self.P[x, y, 1, x, y-1] = fraction
                            counter += fraction
                        if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                            self.P[x, y, 1, x, y+1] = fraction
                            counter += fraction
                        if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                            self.P[x, y, 1, x-1, y] = fraction
                            counter += fraction
                        self.P[x, y, 1, x+1, y] = 1.0 - counter
                    else:
                        self.P[x, y, 1, x, y] = 1.0
                    
                    #South
                    counter = 0.0
                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                            self.P[x, y, 2, x, y-1] = fraction
                            counter += fraction
                        if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                            self.P[x, y, 2, x+1, y] = fraction
                            counter += fraction
                        if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                            self.P[x, y, 2, x-1, y] = fraction
                            counter += fraction
                        self.P[x, y, 2, x, y+1] = 1.0 - counter
                    else:
                        self.P[x, y, 2, x, y] = 1.0
                    
                    #West
                    counter = 0.0
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                            self.P[x, y, 3, x, y-1] = fraction
                            counter += fraction
                        if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                            self.P[x, y, 3, x+1, y] = fraction
                            counter += fraction
                        if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                            self.P[x, y, 3, x, y+1] = fraction
                            counter += fraction
                        self.P[x, y, 3, x-1, y] = 1.0 - counter
                    else:
                        self.P[x, y, 3, x, y] = 1.0
        else:
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    #North
                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 0, x, y-1] = 1.0
                    else:
                        self.P[x, y, 0, x, y] = 1.0
                    #east
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        self.P[x, y, 1, x+1, y] = 1.0
                    else:
                        self.P[x, y, 1, x, y] = 1.0
                    #south
                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 2, x, y+1] = 1.0
                    else:
                        self.P[x, y, 2, x, y] = 1.0
                    #west
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        self.P[x, y, 3, x-1, y] = 1.0
                    else:
                        self.P[x, y, 3, x, y] = 1.0


    def draw_values(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 1.4, 
                        y * self.space_height + self.space_height / 4, 
                        text=str(self.V[x,y]), 
                        fill = "#000", 
                        font = ("RobotoRoman-Bold", int(self.space_width / 7)),
                        tags='V{}{}'.format(x,y))


    def draw_rewards(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] == Actors.goal:
                    self.R[x,y] = 10

                if self.grid_actors[x,y] == Actors.monster:
                    self.R[x,y] = -10

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 5,
                        y * self.space_height + self.space_height / 1.4,
                        text=str(self.R[x,y]),
                        fill = "#000",
                        font = ("RobotoRoman-Bold", int(self.space_width / 7)),
                        tags='R{}{}'.format(x,y))