import numpy as np
from tkinter import Canvas

from Enums import Actors

class Policy_Iteration:   
    def __init__(self, window_size, grid, canvas_grid: Canvas, space_width, space_height):
        self.window_size = window_size
        self.grid_actors = grid
        self.canvas_grid = canvas_grid
        self.space_width = space_width
        self.space_height = space_height

        self.draw_rewards()


    def draw_rewards(self):
        self.reward_values = np.zeros((self.window_size, self.window_size), int)

        for x in range(self.window_size):
            for y in range(self.window_size):
                if self.grid_actors[x,y] == Actors.empty or self.grid_actors[x,y] == Actors.agent or self.grid_actors[x,y] == Actors.obstacle:
                    self.reward_values[x,y] = 0
                    continue

                if self.grid_actors[x,y] == Actors.goal:
                    self.reward_values[x,y] = 10
                    continue

                if self.grid_actors[x,y] == Actors.monster:
                    self.reward_values[x,y] = -10
                    continue

        for x in range(self.window_size):
            for y in range(self.window_size):
                if self.grid_actors[x,y] != 4:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 4,
                        y * self.space_height + self.space_height / 1.4,
                        text="R={}".format(str(self.reward_values[x,y])),
                        fill = "#000",
                        font = ("RobotoRoman-Bold", int(self.space_width / 7)),
                        tags='R{}{}'.format(x,y))


    # def draw_values(self):
    #     for x in range(self.window_size):
    #         for y in range(self.window_size):
    #             if self.grid[x,y] != 4:
    #                 self.canvas_grid.create_text(
    #                     x * self.space_width + self.space_width / 4, 
    #                     y * self.space_height + self.space_height / 1.4, 
    #                     text=str(self.state_values[x,y]), 
    #                     fill = "#000", 
    #                     font = ("RobotoRoman-Bold", int(self.space_width / 4)), 
    #                     tags='V{}{}'.format(x,y))

    
    def step(self, step):
        for i in range(step):
            print("lol")

        #self.draw_values()