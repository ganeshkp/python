def callFunc():
    print("This is ganesh\n")

from tkinter import *
root = Tk()
btn = Button(root, text="Click me!")
#btn.config(command=lambda: print("Hello, Tkinter!"))
btn.config(command=callFunc())
btn.pack(padx=120, pady=30)
root.title("My Tkinter app")
root.mainloop()

