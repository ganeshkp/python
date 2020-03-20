from tkinter import *

root=Tk()

def myClick():
    myLabel=Label(root, text="Look, i clicked button!!")
    myLabel.pack()

myButton=Button(root, text="Click Me!", padx=50, pady=10, command=myClick, fg="blue", bg="red")

myButton.pack()

root.mainloop()