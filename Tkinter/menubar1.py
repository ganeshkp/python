from tkinter import *
def callback(what=None):
    print ("callback =", what)
    if what == 'red':
        b1.config(bg="#ff0000")
    if what == 'blue':
        b2.config(bg="#0000ff")
class Curry:
    """handles arguments for callback functions"""
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        return apply(self.callback, self.args, self.kwargs)
root = Tk()
# create the menubar
menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label="Open", command=Curry(callback, "open"))
filemenu.add_command(label="Save", command=Curry(callback, "save"))
filemenu.add_command(label="Save as", command=Curry(callback, "saveas"))
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.destroy)  # better than root.quit (at least in IDLE)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
# create a toolbar with two buttons
# use Frame(root, borderwidth=2, relief='raised') for more separation
toolbar = Frame(root)
b1 = Button(toolbar, text="red", width=6, command=Curry(callback, "red"))
b1.pack(side=LEFT, padx=2, pady=2)
b2 = Button(toolbar, text="blue", width=6, command=Curry(callback, "blue"))
b2.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)
mainloop()