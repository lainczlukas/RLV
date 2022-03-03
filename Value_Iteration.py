import numpy as np
from tkinter import Canvas

class Value_Iteration:   
    def __init__(self, window_size, grid):
        self.window_size = window_size
        self.state_values = np.zeros((self.window_size, self.window_size), int)

        for x in range(self.window_size):
            for y in range(self.window_size):
                if grid[x,y] == 0 or grid[x,y] != 1:
                    self.state_values[x,y] = 0
                    continue

                if grid[x,y] == 2:
                    self.state_values[x,y] = 10
                    continue

                if grid[x,y] == 3:
                    self.state_values[x,y] = -10
                    continue

                if grid[x,y] == 4:
                    self.state_values[x,y] = -101
                    continue


    def draw_values(self, canvas: Canvas, space_width, space_height):
        for x in range(self.window_size):
            for y in range(self.window_size):
                canvas.create_text(x * space_width + space_width / 2, y * space_height, text=str(self.state_values[x,y]), fill = "#ffffff", font = ("RobotoRoman-Bold", int(space_width / 2)), tags='V{}{}'.format(x,y))