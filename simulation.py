import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *


class Gui:

    def __init__(self, master):

        self.master = master
        self.names = []
        self.displayOnly = []
        self.sliders = []
        master.title("Symulacja")

        for i in range(4):
            self.displayOnly.append(Label(root, text="150"))
            self.displayOnly[i].grid(row=i, column=0)
            self.names.append(Label(root))
            self.names[i].grid(row=i, column=1)

        self.displayOnly[3].config(text="0.01")

        for i in range(5):
            self.sliders.append(Scale(master, from_=0.1, to=2, orient=HORIZONTAL, resolution=0.01))
            self.sliders[i].grid(row=i + 4, column=0)
            self.names.append(Label(root, text=i + 100))
            self.names[i + 4].grid(row=i + 4, column=1)

        self.sliders[0].config(to=100, resolution=1)
        self.sliders[4].config(from_=1, to=300, resolution=1)
        self.sliders[0].set(1)
        self.sliders[1].set(0.2)
        self.sliders[2].set(1)
        self.sliders[3].set(0.5)
        self.sliders[4].set(120)
        self.names[0].config(text="Temperatura czujnika")
        self.names[1].config(text="Temperatura płynu chłodzącego w silniku")
        self.names[2].config(text="Temperatura płynu chłodzącego w chłodnicy")
        self.names[3].config(text="Stopien otwarcia zaworu")
        self.names[4].config(text="Przyrost temperatury silnika w czasie")
        self.names[5].config(text="Współczynnik przyrostu temperatury w chłodnicy")
        self.names[6].config(text="Współczynnik przyrostu temperatury czujnika")
        self.names[7].config(
            text="Współczynnik przyrostu temperatury płynu chłodzącego przy całkowitym otwarciu zaworu")
        self.names[8].config(text="Temperatura zadana")


class Plotter:

    def __init__(self, master):
        self.zmiana = 0.01
        self.max = 0
        self.gui = Gui(master)
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, 100), ylim=(0, 400))
        self.line, = self.ax.plot([], [], lw=2)
        self.anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init, frames=200, interval=50,
                                         blit=True)
        self.x = []
        self.y = []
        plt.show()
    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.updateParameters()
        for i in range(self.max, self.max + 100):
            self.calculateValue()
            self.y.append(self.T_e)
            self.x.append((self.zmiana*i))
        self.max = self.max + 100
        if self.max % 10000 == 0:
            ax = self.max / 100;
            plt.axis([ax, ax + 100, 0, 400])
            plt.draw()
        self.line.set_data(self.x, self.y)
        self.updateGui()
        return self.line,

    def calculateValue(self):
        O2 = round(self.O + self.zmiana * (self.h_max * (self.T_e - self.O)), 2)
        T_e2 = round(self.T_e + self.zmiana * (self.q - self.w * self.h_max * (self.T_e - self.T_r)), 2)
        T_r2 = round(self.T_r + self.zmiana * (self.w * self.h_max * (self.T_e - self.T_r) - self.h_r * self.T_r), 2)
        self.O = min(300, O2)
        self.T_e = min(300, T_e2)
        self.T_r = min(300, T_r2)
        self.w = self.w - 0.5 * (self.T - self.O) / self.T
        self.w = max(min(self.w, 1), 0)

    def updateParameters(self):
        try:
            self.O = float(self.gui.displayOnly[0].cget("text"))
        except:
            exit()
        self.T_e = float(self.gui.displayOnly[1].cget("text"))
        self.T_r = float(self.gui.displayOnly[2].cget("text"))
        self.w = float(self.gui.displayOnly[3].cget("text"))
        self.q = float(self.gui.sliders[0].get())
        self.h_r = float(self.gui.sliders[1].get())
        self.h_e = float(self.gui.sliders[2].get())
        self.h_max = float(self.gui.sliders[3].get())
        self.T = float(self.gui.sliders[4].get())

    def updateGui(self):
        self.gui.displayOnly[0].config(text=round(self.O, 2))
        self.gui.displayOnly[1].config(text=round(self.T_e, 2))
        self.gui.displayOnly[2].config(text=round(self.T_r, 2))
        self.gui.displayOnly[3].config(text=round(self.w, 3))

root = Tk()
simulation = Plotter(root)
root.mainloop()