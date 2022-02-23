from tkinter import *
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
        self.b0.place(x = 615, y = 376, width = 247, height = 35)

        self.scale_size = Scale(from_=2, to=6, orient=HORIZONTAL, length=70, resolution=1, bg = "#E4E4E4")
        self.scale_size.place(x = 704, y = 210)

        self.options = ["Value Iteration", "Policy Iteration"]
        self.algo = StringVar(self.window)
        self.algo.set(self.options[0])
        self.dropdown = OptionMenu(self.window, self.algo, *self.options)
        self.dropdown.config(width=15)
        self.dropdown.place(x = 704, y = 265)

        self.stochastic = IntVar()
        self.check = Checkbutton(bg = "#E4E4E4", variable=self.stochastic)
        self.check.place(x = 704, y = 310)


    def destroy_intro_window(self):
        self.size = self.scale_size.get()
        self.grid = np.zeros((self.size, self.size), int)

        if self.stochastic.get() == 0: 
            self.state = "Deterministic"
        else:
            self.state = "Stochastic"

        self.canvas.delete('all')
        self.b0.destroy()
        self.check.destroy()
        self.dropdown.destroy()
        self.scale_size.destroy()

        self.show_setup_window()


    def show_setup_window(self):
        self.background_img = PhotoImage(file = f"img/background_main.png")
        self.background = self.canvas.create_image(613.5, 250.0, image=self.background_img)

        self.options = ["Agent", "Goal", "Monster", "Obstacle"]
        self.item = StringVar(self.window)
        self.item.set("Choose Item")
        self.dropdown = OptionMenu(self.window, self.item, *self.options)
        self.dropdown.config(width=15)
        self.dropdown.place(x = 60, y = 80)

        self.text_algo = self.canvas.create_text(119.0, 217.5, text = self.algo.get(), fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.text_state = self.canvas.create_text(118.5, 265.5, text = self.state, fill = "#ffffff", font = ("RobotoRoman-Bold", 15))

        self.img0 = PhotoImage(file = f"img/img4.png")
        self.b0 = Button(image = self.img0, borderwidth = 0, highlightthickness = 0, command=self.validate_setup_inputs, relief = "flat")
        self.b0.place(x = 20, y = 319, width = 197, height = 35)

        self.canvas_output = Canvas(self.canvas, bg = "#E4E4E4", height=400, width=250, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_output.place(x = 729, y = 50)

        self.canvas_grid = Canvas(self.canvas, bg = "#E4E4E4", height=400, width=400, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas_grid.place(x = 284, y = 50)

        self.draw_grid()
        self.read_images()
        self.canvas_grid.bind("<Button-1>", self.draw)
        

    def draw_grid(self):
        self.window.update()
        self.space_height = self.canvas_grid.winfo_height() / self.size
        self.space_width = self.canvas_grid.winfo_width() / self.size

        for i in range(1,self.size):
            self.canvas_grid.create_line(0, self.space_height*i, self.canvas_grid.winfo_width(), self.space_height*i)
            self.canvas_grid.create_line(self.space_width*i, 0, self.space_width*i, self.canvas_grid.winfo_height())


    def draw(self, event):
        x_pos = floor(event.x / self.space_height)
        y_pos = floor(event.y / self.space_width)

        if self.item.get() == self.options[0]:
            self.canvas_grid.delete('agent')            
            if self.grid[x_pos, y_pos] == 1:
                self.grid[x_pos, y_pos] = 0                
                return

            if self.grid[x_pos, y_pos] == 2:
                self.canvas_grid.delete('goal')
            elif self.grid[x_pos, y_pos] == 3:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            elif self.grid[x_pos, y_pos] == 4:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            index = np.where(self.grid == 1)
            if len(index[0]) > 0:
                self.grid[index[0][0], index[1][0]] = 0
            self.grid[x_pos,y_pos] = 1
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_agent, anchor=NW, tags='agent')    
        
        if self.item.get() == self.options[1]:
            self.canvas_grid.delete('goal')   
            if self.grid[x_pos, y_pos] == 2:
                self.grid[x_pos, y_pos] = 0
                return
            
            if self.grid[x_pos, y_pos] == 1:
                self.canvas_grid.delete('agent')
            elif self.grid[x_pos, y_pos] == 3:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            elif self.grid[x_pos, y_pos] == 4:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            index = np.where(self.grid == 2)
            if len(index[0]) > 0:
                self.grid[index[0][0], index[1][0]] = 0
            self.grid[x_pos,y_pos] = 2
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_goal, anchor=NW, tags='goal')

        if self.item.get() == self.options[2]:
            if self.grid[x_pos, y_pos] == 3:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
                self.grid[x_pos, y_pos] = 0
                return
            
            if self.grid[x_pos, y_pos] == 1:
                self.canvas_grid.delete('agent')
            elif self.grid[x_pos, y_pos] == 2:
                self.canvas_grid.delete('goal')
            elif self.grid[x_pos, y_pos] == 4:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
            self.grid[x_pos,y_pos] = 3
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_monster, anchor=NW, tags='monster{}{}'.format(x_pos,y_pos))

        if self.item.get() == self.options[3]:
            if self.grid[x_pos, y_pos] == 4:
                self.canvas_grid.delete('obstacle{}{}'.format(x_pos,y_pos))
                self.grid[x_pos, y_pos] = 0
                return
            
            if self.grid[x_pos, y_pos] == 1:
                self.canvas_grid.delete('agent')
            elif self.grid[x_pos, y_pos] == 2:
                self.canvas_grid.delete('goal')
            elif self.grid[x_pos, y_pos] == 3:
                self.canvas_grid.delete('monster{}{}'.format(x_pos,y_pos))
            self.grid[x_pos,y_pos] = 4
            self.canvas_grid.create_image(x_pos * self.space_width, y_pos * self.space_height, image=self.img_obstacle, anchor=NW, tags='obstacle{}{}'.format(x_pos,y_pos))


    def validate_setup_inputs(self):
        if 1 in self.grid and 2 in self.grid:
            self.destroy_setup_window()


    def read_images(self):
        img = Image.open("img/agent.png")
        img = img.resize((int(self.space_width),int(self.space_height)))
        self.img_agent = ImageTk.PhotoImage(img)

        img = Image.open("img/goal.png")
        img = img.resize((int(self.space_width),int(self.space_height)))
        self.img_goal = ImageTk.PhotoImage(img)

        img = Image.open("img/monster.png")
        img = img.resize((int(self.space_width),int(self.space_height)))
        self.img_monster = ImageTk.PhotoImage(img)

        img = Image.open("img/obstacle.png")
        img = img.resize((int(self.space_width),int(self.space_height)))
        self.img_obstacle = ImageTk.PhotoImage(img)


    def destroy_setup_window(self):
        self.canvas.delete(self.text_algo)
        self.canvas.delete(self.text_state)
        self.b0.destroy()
        self.dropdown.destroy()
        self.show_main_window()


    def show_main_window(self):
        self.scale_speed = Scale(from_=1, to=100, orient=HORIZONTAL, length=70, resolution=1, bg = "#E4E4E4")
        self.scale_speed.place(x = 117, y = 115)

        self.scale_gamma = Scale(from_=0, to=1, orient=HORIZONTAL, length=70, resolution=0.05, bg = "#E4E4E4")
        self.scale_gamma.place(x = 117, y = 180)

        self.img0 = PhotoImage(file = f"img/img0.png")
        self.b0 = Button(image = self.img0, borderwidth = 0, highlightthickness = 0, command = self.destroy_main_window, relief = "flat")
        self.b0.place(x = 64, y = 50, width = 110, height = 35)

        self.img1 = PhotoImage(file = f"img/img1.png")
        self.b1 = Button(image = self.img1, borderwidth = 0, highlightthickness = 0, command = self.destroy_main_window, relief = "flat")
        self.b1.place(x = 64, y = 347, width = 110, height = 35)

        self.img2 = PhotoImage(file = f"img/img2.png")
        self.b2 = Button(image = self.img2, borderwidth = 0, highlightthickness = 0, command = self.destroy_main_window, relief = "flat")
        self.b2.place(x = 19, y = 410, width = 200, height = 35)

        self.text_speed = self.canvas.create_text(78.5, 144.5, text = "Speed:", fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.text_gamma = self.canvas.create_text(72.0, 209.5, text = "Gamma:", fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.text_algo = self.canvas.create_text(119.0, 257.5, text = self.algo.get(), fill = "#ffffff", font = ("RobotoRoman-Bold", 15))
        self.text_state = self.canvas.create_text(119.5, 305.5, text = self.state, fill = "#ffffff", font = ("RobotoRoman-Bold", 15))


    def destroy_main_window(self):
        self.canvas.delete('all')
        self.b0.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.canvas_grid.destroy()
        self.canvas_output.destroy()
        self.scale_gamma.destroy()
        self.scale_speed.destroy()
        self.show_intro_window()


if __name__ == "__main__":
    my_window = Window()

    my_window.window.mainloop()