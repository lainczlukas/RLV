from Policy_Iteration import Policy_Iteration
from Value_Iteration import Value_Iteration
from Enums import Actors

from tkinter import *
from tkinter import filedialog
from idlelib.tooltip import Hovertip
from PIL import ImageTk, Image
import numpy as np

from math import floor


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1024x500")
        self.window.configure(bg = "#2a2b2a")
        self.window.title("Reinforcement Learning Visualizator")
        self.window.iconbitmap("img/icon.ico")
        self.window.resizable(False, False)
        self.canvas = Canvas(
            self.window,
            bg = "#2a2b2a",
            height = 500,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.show_intro_window()


    def show_intro_window(self):
        self.background_img = PhotoImage(file = f"img/background_intro.png")
        self.background = self.canvas.create_image(496.0, 249.5, image=self.background_img)

        self.img0 = PhotoImage(file = f"img/img3.png")
        self.b0 = Button(image = self.img0, borderwidth = 0, highlightthickness = 0, command=self.destroy_intro_window, relief = "flat")
        self.b0.place(x = 615, y = 386, width = 247, height = 35)

        self.scale_size = Scale(from_=2, to=6, orient=HORIZONTAL, length=70, resolution=1, bg = "#E4E4E4")
        self.scale_size.place(x = 704, y = 220)

        self.options_algo = ["Value Iteration", "Policy Iteration"]
        self.algo = StringVar(self.window)
        self.algo.set(self.options_algo[0])
        self.dropdown = OptionMenu(self.window, self.algo, *self.options_algo)
        self.dropdown.config(width=15)
        self.dropdown.place(x = 704, y = 275)

        self.deterministic = Scale(from_=0.5, to=1.0, orient=HORIZONTAL, length=70, resolution=0.01, bg = "#E4E4E4")
        self.deterministic.place(x = 704, y = 320)
        self.deterministic.set(1.0)

        self.img1 = PhotoImage(file = f"img/question.png")
        self.question = Label(image=self.img1)
        self.question.place(x=790, y=330)

        self.myTip = Hovertip(self.question,'Represents a probability of ending in a desired state \n 1.0 represents a deterministic environment \n 0.5 represents a random environment', hover_delay=0)        


    def destroy_intro_window(self):
        self.size = self.scale_size.get()

        self.canvas.delete('all')
        self.b0.destroy()
        self.dropdown.destroy()
        self.scale_size.destroy()
        self.question.destroy()

        self.determinism = self.deterministic.get()
        self.deterministic.destroy()

        self.show_setup_window()


    def show_setup_window(self):
        self.background_img = PhotoImage(file = f"img/background_setup.png")
        self.background = self.canvas.create_image(466.5, 250.0, image=self.background_img)

        self.options_actors = ["Place agent", "Place goal", "Place monster", "Place obstacle", "Change reward"]
        self.actor = StringVar(self.window)
        self.actor.set("Choose Action")
        self.dropdown = OptionMenu(self.window, self.actor, *self.options_actors)
        self.dropdown.config(width=15)
        self.dropdown.place(x = 50, y = 80)

        self.img0 = PhotoImage(file = f"img/img4.png")
        self.b0 = Button(image = self.img0, borderwidth = 0, highlightthickness = 0, command=self.validate_setup_inputs, relief = "flat")
        self.b0.place(x = 20, y = 425, width = 197, height = 35)

        self.img1 = PhotoImage(file = f"img/img1.png")
        self.b1 = Button(image = self.img1, borderwidth = 0, highlightthickness = 0, command=self.save_environment, relief = "flat")
        self.b1.place(x = 20, y = 373, width = 197, height = 35)

        self.img2 = PhotoImage(file = f"img/img5.png")
        self.b2 = Button(image = self.img2, borderwidth = 0, highlightthickness = 0, command=self.load_environment, relief = "flat")
        self.b2.place(x = 20, y = 321, width = 197, height = 35)

        self.scale_reward = Scale(from_=-99, to=999, orient=HORIZONTAL, length=70, resolution=1, bg = "#E4E4E4")
        self.scale_reward.place(x = 877, y = 250)

        self.canvas.create_text(810, 270, text = "New reward:", fill = "#E4E4E4", font = ("RobotoRoman-Bold", 14), tags="new_reward")
        self.canvas.create_text(850, 200, text = "Change reward in state:", fill = "#E4E4E4", font = ("RobotoRoman-Bold", 14), tags="change_reward")

        self.img3 = PhotoImage(file = f"img/img6.png")
        self.b3 = Button(image = self.img3, borderwidth = 0, highlightthickness = 0, command= self.validate_change_revard, relief = "flat")
        self.b3.place(x = 760, y = 321, width = 197, height = 35)

        self.myTip = Hovertip(self.b3,'Choose \"Change reward\" from options, \n click on a desired state \n and choose new reward value', hover_delay=0)        

        self.canvas_grid = Canvas(self.canvas, bg = "#E4E4E4", height=400, width=400, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_grid.place(x = 284, y = 50)

        self.canvas.create_rectangle(44, 140, 194, 290, fill="#C0C781", tags='helperBg')
        self.canvas_help = Canvas(self.canvas, bg = "#E4E4E4", height=130, width=130, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_help.place(x = 54, y = 150)
        self.canvas_help.create_text(30, 30, text = "Item", fill = "#000", font = ("RobotoRoman-Bold", 15))
        self.canvas_help.create_text(90, 30, text = "V(s)", fill = "#000", font = ("RobotoRoman-Bold", 15))
        self.canvas_help.create_text(30, 90, text = "R(s)", fill = "#000", font = ("RobotoRoman-Bold", 15))
        self.canvas_help.create_text(90, 90, text = "Policy", fill = "#000", font = ("RobotoRoman-Bold", 14))

        self.window.update()
        self.space_height = self.canvas_grid.winfo_height() / self.size
        self.space_width = self.canvas_grid.winfo_width() / self.size

        self.draw_grid()
        self.load_images()
        self.canvas_grid.bind("<Button-1>", self.draw)

    
    def validate_change_revard(self):
        try:
            if self.x_change_R != None and self.y_change_R != None:
                self.update_reward(self.scale_reward.get(), self.x_change_R, self.y_change_R)
        except AttributeError:
            #TODO:
            pass



    def load_images(self):
        img = Image.open("img/agent.png")
        img = img.resize((int(self.space_width / 2),int(self.space_height / 2)))
        self.img_agent = ImageTk.PhotoImage(img)
        img = Image.open("img/goal.png")
        img = img.resize((int(self.space_width / 2),int(self.space_height / 2)))
        self.img_goal = ImageTk.PhotoImage(img)
        img = Image.open("img/monster.png")
        img = img.resize((int(self.space_width / 2),int(self.space_height / 2)))
        self.img_monster = ImageTk.PhotoImage(img)
        img = Image.open("img/obstacle.png")
        img = img.resize((int(self.space_width),int(self.space_height)))
        self.img_obstacle = ImageTk.PhotoImage(img)


    def draw_grid(self):
        self.window.update()
        self.space_height = self.canvas_grid.winfo_height() / self.size
        self.space_width = self.canvas_grid.winfo_width() / self.size

        for i in range(1,self.size):
            self.canvas_grid.create_line(0, self.space_height*i, self.canvas_grid.winfo_width(), self.space_height*i)
            self.canvas_grid.create_line(self.space_width*i, 0, self.space_width*i, self.canvas_grid.winfo_height())

        self.grid_actors = np.full((self.size, self.size), Actors.empty, Actors)
        self.R = np.full((self.size, self.size), -1)
        self.draw_rewards()
        


    def draw(self, event):
        x_pos = floor(event.x / self.space_height)
        y_pos = floor(event.y / self.space_width)

        if self.actor.get() == self.options_actors[0]:
            self.canvas_grid.delete('agent')            
            if self.grid_actors[x_pos, y_pos] == Actors.agent:
                self.grid_actors[x_pos, y_pos] = Actors.empty        
                return

            if self.grid_actors[x_pos, y_pos] == Actors.goal:
                self.canvas_grid.delete('goal')
                self.update_reward(-1, x_pos, y_pos)
            elif self.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
                self.update_reward(-1, x_pos, y_pos)
            elif self.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
                self.update_reward(-1, x_pos, y_pos)
            index = np.where(self.grid_actors == Actors.agent)
            if len(index[0]) > 0:
                self.grid_actors[index[0][0], index[1][0]] = Actors.empty
            self.grid_actors[x_pos,y_pos] = Actors.agent
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_agent, anchor=NW, tags='agent')
        
        if self.actor.get() == self.options_actors[1]:
            self.canvas_grid.delete('goal')  
            if self.grid_actors[x_pos, y_pos] == Actors.goal:
                self.grid_actors[x_pos, y_pos] = Actors.empty
                self.update_reward(-1, x_pos, y_pos)
                return
            
            if self.grid_actors[x_pos, y_pos] == Actors.agent:
                self.canvas_grid.delete('agent')
            elif self.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            elif self.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            index = np.where(self.grid_actors == Actors.goal)
            if len(index[0]) > 0:
                self.grid_actors[index[0][0], index[1][0]] = Actors.empty
                self.update_reward(-1, index[0][0], index[1][0])
            self.grid_actors[x_pos,y_pos] = Actors.goal
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_goal, anchor=NW, tags='goal')
            self.update_reward(99, x_pos, y_pos)

        if self.actor.get() == self.options_actors[2]:
            if self.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
                self.grid_actors[x_pos, y_pos] = Actors.empty
                self.update_reward(-1, x_pos, y_pos)   
                return
            
            if self.grid_actors[x_pos, y_pos] == Actors.agent:
                self.canvas_grid.delete('agent')
            elif self.grid_actors[x_pos, y_pos] == Actors.goal:
                self.canvas_grid.delete('goal')
            elif self.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            self.grid_actors[x_pos,y_pos] = Actors.monster
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_monster, anchor=NW, tags='monster{}{}'.format(x_pos,y_pos))
            self.update_reward(-20, x_pos, y_pos)

        if self.actor.get() == self.options_actors[3]:
            if self.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
                self.grid_actors[x_pos, y_pos] = Actors.empty
                self.update_reward(-1, x_pos, y_pos)
                return
            
            if self.grid_actors[x_pos, y_pos] == Actors.agent:
                self.canvas_grid.delete('agent')  
            elif self.grid_actors[x_pos, y_pos] == Actors.goal:
                self.canvas_grid.delete('goal')
            elif self.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            self.grid_actors[x_pos,y_pos] = Actors.obstacle
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_obstacle, anchor=NW, tags='obstacle{}{}'.format(x_pos,y_pos))
            text = self.canvas_grid.find_withtag('R{}{}'.format(x_pos,y_pos))
            self.canvas_grid.itemconfig(text, text="")

        if self.actor.get() == self.options_actors[4]:
            self.x_change_R = x_pos
            self.y_change_R = y_pos
            text = self.canvas.find_withtag("change_reward")
            self.canvas.itemconfig(text, text="Change reward in state: {},{}".format(self.x_change_R, self.y_change_R))


    def validate_setup_inputs(self):
        if Actors.agent in self.grid_actors and Actors.goal in self.grid_actors:
            self.destroy_setup_window()
        else:
            print("Wrong Inputs")

    def save_environment(self):
        f = filedialog.asksaveasfile(defaultextension=' .txt', filetypes=[("Text file", '.txt')])

        if f is None:
            return

        f.write(str(self.size) + '\n')

        for x in range(self.size):
            row = ""
            for y in range(self.size):
                row += str(Actors(self.grid_actors[x,y]).value)
            f.write(row + '\n')

        for x in range(self.size):
            row = ""
            for y in range(self.size):
                row += str(self.R[x,y])
                row += ','
            f.write(row + '\n')    

        f.close()


    def load_environment(self):
        path = filedialog.askopenfilename(filetypes= (("Text file","*.txt"), ("All files","*.*")))
        
        if path is None or path == '':
            return

        f = open(path, 'r')

        data = f.readline()
        self.size = int(data)
        self.canvas_grid.delete('all')
        self.draw_grid()
        self.grid_actors = np.full((self.size, self.size), Actors.empty, Actors)

        for x in range(self.size):
            data = f.readline()
            for y in range(self.size):
                self.grid_actors[x,y] = Actors(int(data[y]))

        for x in range(self.size):
            data = f.readline().split(',')
            for y in range(self.size):
                self.R[x,y] = int(data[y])
                if self.grid_actors[x,y] == Actors.obstacle:
                    text = self.canvas_grid.find_withtag('R{}{}'.format(x,y))
                    self.canvas_grid.itemconfig(text, text="")
                else:
                    self.update_reward(self.R[x,y], x, y)

        
        self.load_images()        
        self.draw_actors()

        f.close()

    
    def draw_actors(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid_actors[x,y] == Actors.agent:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_agent, anchor=NW, tags='agent')
                elif self.grid_actors[x,y] == Actors.goal:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_goal, anchor=NW, tags='goal')
                elif self.grid_actors[x,y] == Actors.monster:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_monster, anchor=NW, tags='monster{}{}'.format(x,y))
                elif self.grid_actors[x,y] == Actors.obstacle:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_obstacle, anchor=NW, tags='obstacle{}{}'.format(x,y))


    def destroy_setup_window(self):
        self.canvas_grid.unbind("<Button-1>")
        self.b0.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.scale_reward.destroy()
        self.dropdown.destroy()
        self.canvas.delete('helperBg')
        self.canvas.delete('new_reward')
        self.canvas.delete('change_reward')
        self.canvas.create_rectangle(44, 240, 194, 390, fill="#C0C781", tags='helperBg')
        self.canvas_help.place(x = 54.5, y = 250)
        self.show_main_window()


    def show_main_window(self):
        self.background_img = PhotoImage(file = f"img/background_main.png")
        self.background = self.canvas.create_image(516.5, 250.0, image=self.background_img)

        self.A = [0, 1, 2, 3]
        self.N_actions = len(self.A)
        self.P = np.zeros((self.size, self.size, self.N_actions, self.size, self.size))
        self.set_transitions()

        if self.algo.get() == self.options_algo[0]:
            self.algorithm = Value_Iteration(self.size, self.grid_actors, self.canvas_grid, self.space_width, self.determinism, self.R, self.A, self.P)
        
        if self.algo.get() == self.options_algo[1]:
            self.algorithm = Policy_Iteration(self.size, self.grid_actors, self.canvas_grid, self.space_width, self.determinism, self.R, self.A, self.P)
            self.algorithm.draw_policy()
            pass

        self.scale_speed = Scale(from_=1, to=100, orient=HORIZONTAL, length=70, resolution=1, bg = "#E4E4E4")
        self.scale_speed.place(x = 117, y = 115)

        self.scale_gamma = Scale(from_=0, to=1, orient=HORIZONTAL, length=70, resolution=0.05, bg = "#E4E4E4")
        self.scale_gamma.place(x = 117, y = 180)
        self.scale_gamma.set(0.8)

        self.img0 = PhotoImage(file = f"img/img0.png")
        self.b0 = Button(image = self.img0, borderwidth = 0, highlightthickness = 0, command = self.step, relief = "flat")
        self.b0.place(x = 64, y = 50, width = 110, height = 35)

        self.img2 = PhotoImage(file = f"img/img2.png")
        self.b1 = Button(image = self.img2, borderwidth = 0, highlightthickness = 0, command = self.destroy_main_window, relief = "flat")
        self.b1.place(x = 19, y = 410, width = 200, height = 35)

        self.canvas_Q = Canvas(self.canvas, bg = "#E4E4E4", height=100, width=250, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_Q.place(x = 729, y = 50)

        self.canvas_math = Canvas(self.canvas, bg = "#E4E4E4", height=265, width=250, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_math.place(x = 729, y = 185)
        self.canvas_math.create_text(10, 10, text = "Press Next to render new iteration. \nSpecify in Speed how many \niterations should pass until rendering. \nClick on any state to see Q values.", fill = "#000", font = ("RobotoRoman-Bold", 10), anchor=NW)

        self.canvas.create_text(78.5, 144.5, text = "Speed:", fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.canvas.create_text(72.0, 209.5, text = "Gamma:", fill = "#ffffff", font = ("RobotoRoman-Bold", 15))

        self.algorithm.draw_values()
        self.canvas_grid.bind("<Button-1>", self.show_Q)         

    
    def step(self):
        self.canvas_math.delete('all')
        self.algorithm.step(self.scale_speed.get())


    def show_Q(self, event):
        self.canvas_Q.delete('all')

        x = floor(event.x / self.space_height)
        y = floor(event.y / self.space_width)
        Q = self.algorithm.get_Q(x, y)

        if self.grid_actors[x,y] == Actors.obstacle:
            self.canvas_Q.create_text(20,10, text = "Not a state".format(x,y,round(Q[0], 2)), fill = "#000", font = ("RobotoRoman-Bold", 20), anchor=NW)
            return

        if self.grid_actors[x,y] == Actors.goal or self.grid_actors[x,y] == Actors.monster:
            self.canvas_Q.create_text(20,10, text = "Terminal state".format(x,y,round(Q[0], 2)), fill = "#000", font = ("RobotoRoman-Bold", 20), anchor=NW)
            return
        
        self.canvas_Q.create_text(20,10, text = "Q({}{},N) = {}".format(x,y,round(Q[0], 2)), fill = "#000", font = ("RobotoRoman-Bold", 10), anchor=NW)
        self.canvas_Q.create_text(20,30, text = "Q({}{},E) = {}".format(x,y,round(Q[1], 2)), fill = "#000", font = ("RobotoRoman-Bold", 10), anchor=NW)
        self.canvas_Q.create_text(20,50, text = "Q({}{},S) = {}".format(x,y,round(Q[2], 2)), fill = "#000", font = ("RobotoRoman-Bold", 10), anchor=NW)
        self.canvas_Q.create_text(20,70, text = "Q({}{},W) = {}".format(x,y,round(Q[3], 2)), fill = "#000", font = ("RobotoRoman-Bold", 10), anchor=NW)


    def destroy_main_window(self):
        self.canvas.delete('all')
        self.b0.destroy()
        self.b1.destroy()
        self.canvas_grid.destroy()
        self.canvas_Q.destroy()
        self.canvas_math.destroy()
        self.canvas_help.destroy()
        self.scale_gamma.destroy()
        self.scale_speed.destroy()
        self.show_intro_window()

    def draw_rewards(self):
        for x in range(self.size):
            for y in range(self.size):
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


    def set_transitions(self):
        for x in range(self.size):
            for y in range(self.size):
                #North
                counter = 0
                if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                    self.P[x, y, 0, x, y-1] = self.determinism

                    if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        counter += 1
                    if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        counter += 1
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        counter += 1
                    
                    wrong_way_probability = (1 - self.determinism) / counter

                    if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 0, x, y+1] = wrong_way_probability
                    if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        self.P[x, y, 0, x+1, y] = wrong_way_probability
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        self.P[x, y, 0, x-1, y] = wrong_way_probability
                else:
                    self.P[x, y, 0, x, y] = 1.0

                #East
                counter = 0
                if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                    self.P[x, y, 1, x+1, y] = self.determinism

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        counter += 1
                    if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        counter += 1
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        counter += 1
                    
                    wrong_way_probability = (1 - self.determinism) / counter

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 1, x, y-1] = wrong_way_probability
                    if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 1, x, y+1] = wrong_way_probability
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        self.P[x, y, 1, x-1, y] = wrong_way_probability
                else:
                    self.P[x, y, 1, x, y] = 1.0
                
                #South
                counter = 0.0
                if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                    self.P[x, y, 2, x, y+1] = self.determinism

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        counter += 1
                    if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        counter += 1
                    if x != 0 and self.grid_actors[x-1,y] != Actors.obstacle:
                        counter += 1
                    
                    wrong_way_probability = (1 - self.determinism) / counter

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 2, x, y-1] = wrong_way_probability
                    if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
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
                    if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        counter += 1
                    if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        counter += 1

                    wrong_way_probability = (1 - self.determinism) / counter

                    if y != 0 and self.grid_actors[x,y-1] != Actors.obstacle:
                        self.P[x, y, 3, x, y-1] = wrong_way_probability
                    if x != self.size - 1 and self.grid_actors[x+1,y] != Actors.obstacle:
                        self.P[x, y, 3, x+1, y] = wrong_way_probability
                    if y != self.size - 1 and self.grid_actors[x,y+1] != Actors.obstacle:
                        self.P[x, y, 3, x, y+1] = wrong_way_probability
                else:
                    self.P[x, y, 3, x, y] = 1.0



if __name__ == "__main__":
    my_window = Window()

    my_window.window.mainloop()