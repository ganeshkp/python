from tkinter import *

root=Tk()

e=Entry(root, width=50, bg="blue", fg="white", borderwidth=2)
e.pack()
e.insert(0,"Enter Your name:")

def myClick():
    hello="Hello "+e.get()
    myLabel=Label(root, text=hello)
    myLabel.pack()

myButton=Button(root, text="Enter Your name!", padx=50, pady=10, command=myClick, fg="blue", bg="red")
myButton.pack()

root.mainloop()