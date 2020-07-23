import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib.request
import json

import pandas as pd
import numpy as np
from datetime import datetime

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(6, 4), dpi=100)
a = f.add_subplot(111)
samples = 0


def animate(i):
    xData = []
    dataLink = "https://blockchain.info/ticker"
    data = urllib.request.urlopen(dataLink).read().decode("ascii", "ignore")
    data = json.loads(data)
    # print(data["USD"]["last"]) #debug data from API
    data = pd.DataFrame(data)
    # print(data)

    # buys = data[(data["last"]=="bid")]
    buys = data["USD"]
    print(buys)
    # buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
    # buyDates = (buys["datestamp"]).tolist()

    # sells = data[(data["type"]=="ask")]
    sells = data["USD"]
    print(sells)
    # sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
    # sellDates = (sells["datestamp"]).tolist()
    global samples
    samples = datetime.now()
    xData.append(samples)
    a.clear()
    a.plot_date(xData, buys["buy"])
    a.plot_date(xData, sells["sell"])


class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="")  # set icon 16x16
        tk.Tk.wm_title(self, "BTC Client")  # set title

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, BTCe_page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def qf(param):
    print(param)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ALPHA BTC trading application", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        label = tk.Label(self, text="Use at your own risk. There is no promise of warranty", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree", command=quit)
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to home", command=lambda: controller.show_frame(StartPage))
        button1.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()


class BTCe_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        # canvas.show()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=100)
app.mainloop()