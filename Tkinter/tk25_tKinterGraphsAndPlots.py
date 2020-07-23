from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = Tk()
root.title('Learn to code at codemy.com')
root.geometry("700x700")

def graph():
    # The three commented lines all generate graph on a new window, which I didn't want
    #house_prices = np.random.normal(200000, 2500, 5000)
    #plt.hist(house_prices, 200)
    #plt.show()
    f = Figure()
    a = f.gca()  # gca = "get current axes" to use for the plot. Could also be done using f.add_subplot(111) but this is cleaner since we only have 1 plot.
    t = np.arange(0.0,3.0,0.01)
    s = np.sin(2*np.pi*t)
    a.plot(t,s)
    dataPlot = FigureCanvasTkAgg(f, master=root)
    dataPlot.show()
    dataPlot.get_tk_widget().pack()



my_button = Button(root, text = "Graph it!", command = graph)
my_button.pack()

root.mainloop()