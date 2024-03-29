import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        label_a = tk.Label(self, text="Label A", bg="yellow")
        label_b = tk.Label(self, text="Label B", bg="orange")
        label_c = tk.Label(self, text="Label C", bg="red")
        label_d = tk.Label(self, text="Label D", bg="green")
        label_e = tk.Label(self, text="Label E", bg="blue")
        label_f = tk.Label(self, text="Label F", bg="yellow")
        opts = { 'ipadx': 10, 'ipady': 10, 'fill': tk.BOTH }
        label_a.pack(side=tk.TOP, **opts)
        label_b.pack(side=tk.TOP, **opts)
        label_c.pack(side=tk.LEFT, **opts)
        label_d.pack(side=tk.LEFT, **opts)
        label_e.pack(side=tk.LEFT, **opts)
        label_f.pack(side=tk.BOTTOM, **opts)

if __name__ == "__main__":
    app = App()
    app.mainloop()