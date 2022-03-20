import numpy as np
from tkinter import Canvas

from Enums import Actors

class Value_Iteration:   
    def __init__(self, grid_size, grid_actors, canvas_grid: Canvas, space_width, determinism, R, A, P):
        self.grid_size = grid_size
        self.grid_actors = grid_actors
        self.canvas_grid = canvas_grid
        self.space_width = space_width
        self.space_height = self.space_width
        self.determinism = determinism
        self.R = R
        self.A = A
        self.P = P
        
        self.V = np.zeros((self.grid_size, self.grid_size), float)

        self.N_actions = len(self.A)

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
                        action_values = self.get_Q(x, y)                 
                        self.V[x, y] = max(action_values)
                        delta = max(delta, abs(prev_value - self.V[x, y]))
            
            if delta < self.theta:
                self.update_values()
                self.calculate_policy()
                return
        
        self.update_values()


    def get_Q(self, x, y):
        action_values = list()
        for action in range(self.N_actions):
            action_value = sum([self.P[x, y, action, x1, y1] * (self.R[x1, y1] + self.gamma * self.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])
            action_values.append(action_value)

        return action_values             

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


