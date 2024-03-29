from tkinter import *
import numpy as np

from Enums import Actors, Directions

from random import choice

class Environment:
    def __init__(self, grid_size, canvas_grid: Canvas, space_width, determinism):
        self.grid_size = grid_size
        self.grid_actors = np.full((self.grid_size, self.grid_size), Actors.empty, Actors)
        self.canvas_grid = canvas_grid

        self.determinism = determinism

        self.space_width = space_width
        self.space_height = self.space_width

        self.A = [0, 1, 2, 3]
        self.N_actions = len(self.A)
        self.R = np.full((self.grid_size, self.grid_size), -1)
        self.P = np.zeros((self.grid_size, self.grid_size, self.N_actions, self.grid_size, self.grid_size))
        self.V = np.zeros((self.grid_size, self.grid_size), float)
        self.policy = np.zeros((self.grid_size, self.grid_size), int)

        self.equations = {}
        self.set_transitions()


    def update_values(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle:
                    text = self.canvas_grid.find_withtag('V{}{}'.format(x,y))
                    self.canvas_grid.itemconfig(text, text=str(round(self.V[x,y], 2)))
        
       
    def update_values_on(self,x,y):
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


    def draw_rewards(self):
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

    
    def update_reward(self, reward, x, y):
        text = self.canvas_grid.find_withtag('R{}{}'.format(x,y))
        self.canvas_grid.itemconfig(text, text=str(round(reward, 2)))
        self.R[x,y] = reward


    def update_policy(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.obstacle:
                    text = self.canvas_grid.find_withtag('P{}{}'.format(x,y))
                    self.canvas_grid.itemconfig(text, text=str(Directions(self.policy[x,y]).name))


    def update_policy_on(self,x,y):
        text = self.canvas_grid.find_withtag('P{}{}'.format(x,y))
        self.canvas_grid.itemconfig(text, text=str(Directions(self.policy[x,y]).name))


    def draw_policy(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_actors[x,y] != Actors.goal and self.grid_actors[x,y] != Actors.monster and self.grid_actors[x,y] != Actors.obstacle:
                    self.canvas_grid.create_text(
                        x * self.space_width + self.space_width / 1.4, 
                        y * self.space_height + self.space_height / 1.4, 
                        text=str(Directions(self.policy[x,y]).name),
                        fill = "#000", 
                        font = ("RobotoRoman-Bold", int(self.space_width / 7)),
                        tags='P{}{}'.format(x,y))


    def set_transitions(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                #North
                counter = 0
                if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                    self.P[x, y, 0, x, y-1] = self.determinism

                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        counter += 1
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        counter += 1
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        counter += 1
                    
                    if counter != 0:
                        wrong_way_probability = (1 - self.determinism) / counter
                    else:
                        self.P[x, y, 0, x, y-1] = 1

                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 0, x, y+1] = wrong_way_probability
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        self.P[x, y, 0, x+1, y] = wrong_way_probability
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        self.P[x, y, 0, x-1, y] = wrong_way_probability
                else:
                    self.P[x, y, 0, x, y] = 1.0

                #East
                counter = 0
                if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                    self.P[x, y, 1, x+1, y] = self.determinism

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        counter += 1
                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        counter += 1
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        counter += 1
                    
                    if counter != 0:
                        wrong_way_probability = (1 - self.determinism) / counter
                    else:
                        self.P[x, y, 1, x+1, y] = 1

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 1, x, y-1] = wrong_way_probability
                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 1, x, y+1] = wrong_way_probability
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        self.P[x, y, 1, x-1, y] = wrong_way_probability
                else:
                    self.P[x, y, 1, x, y] = 1.0
                
                #South
                counter = 0.0
                if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                    self.P[x, y, 2, x, y+1] = self.determinism

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        counter += 1
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        counter += 1
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        counter += 1
                    
                    if counter != 0:
                        wrong_way_probability = (1 - self.determinism) / counter
                    else:
                        self.P[x, y, 2, x, y+1] = 1

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 2, x, y-1] = wrong_way_probability
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        self.P[x, y, 2, x+1, y] = wrong_way_probability
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        self.P[x, y, 2, x-1, y] = wrong_way_probability
                else:
                    self.P[x, y, 2, x, y] = 1.0
                
                #West
                counter = 0.0
                if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                    self.P[x, y, 3, x-1, y] = self.determinism

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        counter += 1
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        counter += 1
                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        counter += 1

                    if counter != 0:
                        wrong_way_probability = (1 - self.determinism) / counter
                    else:
                        self.P[x, y, 3, x-1, y] = 1

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 3, x, y-1] = wrong_way_probability
                    if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        self.P[x, y, 3, x+1, y] = wrong_way_probability
                    if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 3, x, y+1] = wrong_way_probability
                else:
                    self.P[x, y, 3, x, y] = 1.0


    def update_size(self, grid_size):
        self.grid_size = grid_size
        self.grid_actors = np.full((self.grid_size, self.grid_size), Actors.empty, Actors)
        self.R = np.full((self.grid_size, self.grid_size), -1)
        self.P = np.zeros((self.grid_size, self.grid_size, self.N_actions, self.grid_size, self.grid_size))
        self.V = np.zeros((self.grid_size, self.grid_size), float)
        self.policy = np.zeros((self.grid_size, self.grid_size), int)

        self.space_height = self.canvas_grid.winfo_height() / self.grid_size
        self.space_width = self.canvas_grid.winfo_width() / self.grid_size

    
    def set_agent_img(self, img):
        self.img_agent = img


    def draw_agent(self, state):
        x = state[0]
        y = state[1]
        self.canvas_grid.delete('agent')            

        index = np.where(self.grid_actors == Actors.agent)
        if len(index[0]) > 0:
            self.grid_actors[index[0][0], index[1][0]] = Actors.empty
        self.grid_actors[x,y] = Actors.agent
        self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_agent, anchor=NW, tags='agent')


    def get_new_state(self, action, state):
        options = []
        x = state[0]
        y = state[1]

        if x != self.grid_size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
            chance = self.P[x, y, action, x + 1, y] * 100
            for _ in range(int(chance)):
                options.append((x + 1, y))
        if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
            chance = self.P[x, y, action, x - 1, y] * 100
            for _ in range(int(chance)):
                options.append((x - 1, y))

        if y != self.grid_size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
            chance = self.P[x, y, action, x, y + 1] * 100
            for _ in range(int(chance)):
                options.append((x, y + 1))
        
        if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
            chance = self.P[x, y, action, x, y - 1] * 100
            for _ in range(int(chance)):
                options.append((x, y - 1))

        if len(options) == 0:
            options.append(state)    
        next_state = choice(options)

        reward = self.R[next_state]
        done = False
        if self.grid_actors[next_state] == Actors.goal or self.grid_actors[next_state] == Actors.monster:
            done = True

        return next_state, reward, done


    def init_equation(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                equation = "Q({},{}) = [N=0,E=0,S=0,W=0]".format(x,y)   
                self.equations['{}{}'.format(x,y)] = []             
                self.equations['{}{}'.format(x,y)].append(equation)