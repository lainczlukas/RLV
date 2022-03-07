import numpy as np
from tkinter import Canvas

class Value_Iteration:   
    def __init__(self, window_size, grid, canvas_grid: Canvas, space_width, space_height):
        self.window_size = window_size
        self.grid = grid
        self.canvas_grid = canvas_grid
        self.space_width = space_width
        self.space_height = space_height

        self.state_values = np.zeros((self.window_size, self.window_size), int)

        for x in range(self.window_size):
            for y in range(self.window_size):
                if self.grid[x,y] == 0 or self.grid[x,y] == 1 or self.grid[x,y] == 4:
                    self.state_values[x,y] = 0
                    continue

                if self.grid[x,y] == 2:
                    self.state_values[x,y] = 10
                    continue

                if self.grid[x,y] == 3:
                    self.state_values[x,y] = -10
                    continue


    def draw_values(self):
        for x in range(self.window_size):
            for y in range(self.window_size):
                if self.grid[x,y] != 4:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 4, 
                        y * self.space_height + self.space_height / 1.4, 
                        text=str(self.state_values[x,y]), 
                        fill = "#000", 
                        font = ("RobotoRoman-Bold", int(self.space_width / 4)), 
                        tags='V{}{}'.format(x,y))

    
    def step(self, step):
        for i in range(step):
            print("lol")

        self.draw_values()