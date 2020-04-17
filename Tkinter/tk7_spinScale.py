import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.spinbox = tk.Spinbox(self, from_=0, to=50)
        self.scale = tk.Scale(self, from_=0, to=50, resolution=0.2,
                            #orient=tk.HORIZONTAL)
                              orient=tk.HORIZONTAL)
        self.btn = tk.Button(self, text="Print values",
                            command=self.print_values)
        self.spinbox.pack()
        self.scale.pack()
        self.btn.pack()

    def print_values(self):
        if float(self.spinbox.get())==2.0:
            print("PRINTED")
        print("Spinbox: {}".format(self.spinbox.get()))
        print("Scale: {}".format(self.scale.get()))

if __name__ == "__main__":
    app = App()
    app.mainloop()