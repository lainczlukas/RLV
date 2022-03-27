import numpy as np
from tkinter import Canvas

from Enums import Actors

class Policy_Iteration:   
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
        self.policy = np.zeros((self.grid_size, self.grid_size), int)
        self.Q = {}

        self.N_actions = len(self.A)

        self.gamma = 0.8
        self.epsilon = 0.5

        self.converged = False


    def step(self, step):
        if self.converged:
            return
        
        for _ in range(step):
            old_policy = self.policy.copy()
            self.policy_evaluation()
            self.policy_improvement()
            self.update_values()
            self.update_policy()

            if all(old_policy[x,y] == self.policy[x,y] for x in range(self.grid_size) for y in range(self.grid_size)):
                self.converged = True
                return


    def policy_evaluation(self):
        self.V = np.zeros((self.grid_size, self.grid_size), float)

        while True:
            old_values = self.V.copy()

            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        action = self.policy[x,y]
                        self.V[x,y] = sum([self.P[x, y, action, x1, y1] * (self.R[x1, y1] + self.gamma * self.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])

            if all(abs(old_values[x,y] - self.V[x,y]) < self.epsilon for x in range(self.grid_size) for y in range(self.grid_size)):
                break


    def policy_improvement(self):
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster:
                        Q_values = []
                        for action in range(self.N_actions):
                            Q_values.append(sum(([self.P[x, y, action, x1, y1] * (self.R[x1, y1] + self.gamma * self.V[x1, y1]) for x1 in range(self.grid_size) for y1 in range(self.grid_size)])))
                        
                        self.Q["{}{}".format(x,y)] = Q_values
                        self.policy[x,y] = np.argmax(Q_values)


    def get_Q(self, x, y):
        key = "{}{}".format(x,y)
        if key in self.Q:
            return self.Q[key]
        return [0.0,0.0,0.0,0.0]           

    def update_policy(self):
        direction = {0: "N", 1: "E", 2: "S", 3:"W"}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle:
                    text = self.canvas_grid.find_withtag('P{}{}'.format(x,y))
                    self.canvas_grid.itemconfig(text, text=direction[self.policy[x,y]])


    def draw_policy(self):
        direction = {0: "N", 1: "E", 2: "S", 3:"W"}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster and self.grid_actors[x,y] != Actors.obstacle:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 1.4, 
                        y * self.space_height + self.space_height / 1.4, 
                        text=direction[self.policy[x,y]], 
                        fill = "#000", 
                        font = ("RobotoRoman-Bold", int(self.space_width / 7)),
                        tags='P{}{}'.format(x,y))


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