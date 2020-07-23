import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class App:
    def __init__(self, master, increment=2, height=10):
        self.increment = increment
        # Create a container
        frame = tkinter.Frame(master)
        # Make buttons...
        self.button_left = tkinter.Button(frame,text="< Move Left",
                                        command=self.move_left)
        self.button_left.pack(side="left")
        self.button_right = tkinter.Button(frame,text="Move Right >",
                                        command=self.move_right)
        self.button_right.pack(side="left")

        fig = Figure()
        ax = fig.add_subplot(111)
        x = [3]*height
        y = range(height)
        #so that it's a tuple
        self.line, = ax.plot(x, y)
        self.canvas = FigureCanvasTkAgg(fig, master=master)
        #self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def move_left(self):
        x, y = self.line.get_data()
        self.line.set_xdata(x-self.increment)
        x, y = self.line.get_data()
        print ("x: {0}".format(x))
        print ("y: {0}".format(y))
        #self.canvas.draw()
        self.canvas.blit()


    def move_right(self):
        x, y = self.line.get_data()
        self.line.set_xdata(x+self.increment)
        x, y = self.line.get_data()
        print ("x: {0}".format(x))
        print ("y: {0}".format(y))
        #self.canvas.draw()
        self.canvas.blit()

root = tkinter.Tk()
app = App(root)
root.mainloop()