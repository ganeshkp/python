import tkinter as tk

class SwitchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.var = tk.StringVar()
        self.var.set("OFF")

        self.cb = tk.Checkbutton(self, text="Active?", variable=self.var,
                                            onvalue="ON", offvalue="OFF",
                                            command=self.print_value)

        self.cb.pack()

    def print_value(self):
        if self.var.get()=="ON":
            print("SELECTED")
        else:
            print("DE-SELECTED")
        print(self.var.get())

if __name__ == "__main__":
    app = SwitchApp()
    app.mainloop()