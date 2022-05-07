from Policy_Iteration import Policy_Iteration
from Value_Iteration import Value_Iteration
from Q_learning import Q_learning
from Enums import Actors
from Environment import Environment

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

        self.myTip = Hovertip(self.question,' Represents a probability of ending in a desired state \n 1.0 represents a 100% probability - a deterministic environment \n 0.5 represents a 50% probability of ending in a desired state and \n a 50% probability of ending in other possible state \n this probability is equally distributed \n among every other neighboring state', hover_delay=0)        


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
        self.scale_reward.place(x = 877, y = 330)

        self.canvas.create_text(810, 350, text = "New reward:", fill = "#E4E4E4", font = ("RobotoRoman-Bold", 14), tags="new_reward")
        self.canvas.create_text(850, 290, text = "Change reward in state:", fill = "#E4E4E4", font = ("RobotoRoman-Bold", 14), tags="change_reward")

        self.img3 = PhotoImage(file = f"img/img6.png")
        self.b3 = Button(image = self.img3, borderwidth = 0, highlightthickness = 0, command= self.validate_change_revard, relief = "flat")
        self.b3.place(x = 760, y = 401, width = 197, height = 35)       

        self.canvas_grid = Canvas(self.canvas, bg = "#E4E4E4", height=400, width=400, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_grid.place(x = 284, y = 50)

        self.canvas.create_rectangle(44, 140, 194, 290, fill="#C0C781", tags='helperBg')
        self.canvas_help = Canvas(self.canvas, bg = "#E4E4E4", height=130, width=130, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_help.place(x = 54, y = 150)
        self.canvas_help.create_text(30, 30, text = "Item", fill = "#000", font = ("RobotoRoman-Bold", 15))
        self.canvas_help.create_text(90, 30, text = "V(s)", fill = "#000", font = ("RobotoRoman-Bold", 15))
        self.canvas_help.create_text(30, 90, text = "R(s)", fill = "#000", font = ("RobotoRoman-Bold", 15))
        self.canvas_help.create_text(90, 90, text = "Policy", fill = "#000", font = ("RobotoRoman-Bold", 14))
        self.canvas.create_text(710, 50, text = " Click on top left widget, choose an actor \n and click on a gridworld state to place/remove it. \n You need to place at least agent and goal \n to start environment. \n Choose \"Change reward\" from options, \n click on a desired state \n and choose new reward value. \n You can save your environment and load it later. \n Number in a bottom left corner of a state represents \n reward agent obtains by getting to the state. \n After starting the algoritm policy and value \n wil be calculated and rendered for every state.", fill = "#E4E4E4", font = ("RobotoRoman-Bold", 10), anchor=NW, tags="setupHelp")
        self.window.update()
        self.space_height = self.canvas_grid.winfo_height() / self.size
        self.space_width = self.canvas_grid.winfo_width() / self.size

        self.load_images()
        self.canvas_grid.bind("<Button-1>", self.draw)

        self.environment = Environment(self.size, self.canvas_grid, self.space_width, self.determinism)
        self.draw_grid()

    
    def validate_change_revard(self):
        try:
            if self.x_change_R != None and self.y_change_R != None:
                self.environment.update_reward(self.scale_reward.get(), self.x_change_R, self.y_change_R)
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

        self.environment.draw_rewards()
        

    def draw(self, event):
        x_pos = floor(event.x / self.space_height)
        y_pos = floor(event.y / self.space_width)

        if self.actor.get() == self.options_actors[0]:
            self.canvas_grid.delete('agent')            
            if self.environment.grid_actors[x_pos, y_pos] == Actors.agent:
                self.environment.grid_actors[x_pos, y_pos] = Actors.empty        
                return

            if self.environment.grid_actors[x_pos, y_pos] == Actors.goal:
                self.canvas_grid.delete('goal')
                self.environment.update_reward(-1, x_pos, y_pos)
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
                self.environment.update_reward(-1, x_pos, y_pos)
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
                self.environment.update_reward(-1, x_pos, y_pos)
            index = np.where(self.environment.grid_actors == Actors.agent)
            if len(index[0]) > 0:
                self.environment.grid_actors[index[0][0], index[1][0]] = Actors.empty
            self.environment.grid_actors[x_pos,y_pos] = Actors.agent
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_agent, anchor=NW, tags='agent')
        
        if self.actor.get() == self.options_actors[1]:
            self.canvas_grid.delete('goal')  
            if self.environment.grid_actors[x_pos, y_pos] == Actors.goal:
                self.environment.grid_actors[x_pos, y_pos] = Actors.empty
                self.environment.update_reward(-1, x_pos, y_pos)
                return
            
            if self.environment.grid_actors[x_pos, y_pos] == Actors.agent:
                self.canvas_grid.delete('agent')
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            index = np.where(self.environment.grid_actors == Actors.goal)
            if len(index[0]) > 0:
                self.environment.grid_actors[index[0][0], index[1][0]] = Actors.empty
                self.environment.update_reward(-1, index[0][0], index[1][0])
            self.environment.grid_actors[x_pos,y_pos] = Actors.goal
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_goal, anchor=NW, tags='goal')
            self.environment.update_reward(99, x_pos, y_pos)

        if self.actor.get() == self.options_actors[2]:
            if self.environment.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
                self.environment.grid_actors[x_pos, y_pos] = Actors.empty
                self.environment.update_reward(-1, x_pos, y_pos)   
                return
            
            if self.environment.grid_actors[x_pos, y_pos] == Actors.agent:
                self.canvas_grid.delete('agent')
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.goal:
                self.canvas_grid.delete('goal')
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            self.environment.grid_actors[x_pos,y_pos] = Actors.monster
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_monster, anchor=NW, tags='monster{}{}'.format(x_pos,y_pos))
            self.environment.update_reward(-20, x_pos, y_pos)

        if self.actor.get() == self.options_actors[3]:
            if self.environment.grid_actors[x_pos, y_pos] == Actors.obstacle:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
                self.environment.grid_actors[x_pos, y_pos] = Actors.empty
                self.environment.update_reward(-1, x_pos, y_pos)
                return
            
            if self.environment.grid_actors[x_pos, y_pos] == Actors.agent:
                self.canvas_grid.delete('agent')  
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.goal:
                self.canvas_grid.delete('goal')
            elif self.environment.grid_actors[x_pos, y_pos] == Actors.monster:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            self.environment.grid_actors[x_pos,y_pos] = Actors.obstacle
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_obstacle, anchor=NW, tags='obstacle{}{}'.format(x_pos,y_pos))
            text = self.canvas_grid.find_withtag('R{}{}'.format(x_pos,y_pos))
            self.canvas_grid.itemconfig(text, text="")

        if self.actor.get() == self.options_actors[4]:
            self.x_change_R = x_pos
            self.y_change_R = y_pos
            if self.environment.grid_actors[self.x_change_R, self.y_change_R] != Actors.obstacle:
                text = self.canvas.find_withtag("change_reward")
                self.canvas.itemconfig(text, text="Change reward in state: {},{}".format(self.x_change_R, self.y_change_R))


    def validate_setup_inputs(self):
        if Actors.agent in self.environment.grid_actors and Actors.goal in self.environment.grid_actors:
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
                row += str(Actors(self.environment.grid_actors[x,y]).value)
            f.write(row + '\n')

        for x in range(self.size):
            row = ""
            for y in range(self.size):
                row += str(self.environment.R[x,y])
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
        self.window.update()
        self.environment.update_size(self.size)
        self.canvas_grid.delete('all')
        self.draw_grid()

        for x in range(self.size):
            data = f.readline()
            for y in range(self.size):
                self.environment.grid_actors[x,y] = Actors(int(data[y]))

        for x in range(self.size):
            data = f.readline().split(',')
            for y in range(self.size):
                self.environment.R[x,y] = int(data[y])
                if self.environment.grid_actors[x,y] == Actors.obstacle:
                    text = self.canvas_grid.find_withtag('R{}{}'.format(x,y))
                    self.canvas_grid.itemconfig(text, text="")
                else:
                    self.environment.update_reward(self.environment.R[x,y], x, y)

        self.load_images()        
        self.draw_actors()
        f.close()


    def draw_actors(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.environment.grid_actors[x,y] == Actors.agent:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_agent, anchor=NW, tags='agent')
                elif self.environment.grid_actors[x,y] == Actors.goal:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_goal, anchor=NW, tags='goal')
                elif self.environment.grid_actors[x,y] == Actors.monster:
                    self.canvas_grid.create_image(x * self.space_width, y * self.space_height, image=self.img_monster, anchor=NW, tags='monster{}{}'.format(x,y))
                elif self.environment.grid_actors[x,y] == Actors.obstacle:
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
        self.canvas.delete('setupHelp')
        self.canvas_help.destroy()
        self.show_main_window()


    def show_main_window(self):
        self.background_img = PhotoImage(file = f"img/background_main.png")
        self.background = self.canvas.create_image(612.5, 250.0, image=self.background_img)

        self.environment.set_transitions()

        if self.algo.get() == self.options_algo[0]:
            self.algorithm = Value_Iteration(self.environment)
            self.equation_img = PhotoImage(file = f"img/VI.png")
            self.canvas.create_image(854, 100, image=self.equation_img)

        if self.algo.get() == self.options_algo[1]:
            self.algorithm = Policy_Iteration(self.environment)
            self.equation_img = PhotoImage(file = f"img/PI.png")
            self.canvas.create_image(854, 100, image=self.equation_img)
            self.environment.draw_policy()

        # if self.algo.get() == self.options_algo[2]:
        #     self.algorithm = Q_learning(self.environment)

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

        self.canvas_math = Canvas(self.canvas, bg = "#E4E4E4", height=265, width=250, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_math.place(x = 729, y = 185)

        self.canvas.create_text(78.5, 144.5, text = "Speed:", fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.canvas.create_text(72.0, 209.5, text = "Gamma:", fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.canvas.create_text(10, 280, text = """ Press Next to render new iteration. \n Specify in Speed how many \n iterations should pass before rendering. 
 Click on any state and click next \n to see how state value was calculated.
 Press next until algorithm converges.\n""", fill = "#E4E4E4", font = ("RobotoRoman-Bold", 9), anchor=NW)

        self.environment.draw_values()
        self.canvas_grid.bind("<Button-1>", self.render_math)         


    def step(self):
        self.canvas_math.delete('all')
        self.algorithm.step(self.scale_speed.get())


    def render_math(self, event):
        self.canvas_math.delete('all')
        x = floor(event.x / self.space_height)
        y = floor(event.y / self.space_width)
        if self.environment.grid_actors[x,y] != Actors.obstacle:
            if self.environment.equations:
                if self.environment.grid_actors[x,y] == Actors.goal or self.environment.grid_actors[x,y] == Actors.monster:
                    self.canvas_math.create_text(10, 10, text="Terminal state", anchor=NW)
                else:
                    for i, equation in enumerate(self.environment.equations["{}{}".format(x,y)]):
                        self.canvas_math.create_text(10, 10 + 65 * i, text=equation, anchor=NW)
            else:
                self.canvas_math.create_text(10, 10, text="All state values were initialised to 0", anchor=NW)


    def destroy_main_window(self):
        self.canvas.delete('all')
        self.b0.destroy()
        self.b1.destroy()
        self.canvas_grid.destroy()
        self.canvas_math.destroy()
        self.canvas_help.destroy()
        self.scale_gamma.destroy()
        self.scale_speed.destroy()
        self.show_intro_window()


if __name__ == "__main__":
    my_window = Window()

    my_window.window.mainloop()