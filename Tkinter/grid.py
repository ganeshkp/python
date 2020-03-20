from tkinter import *

root=Tk()

myLabel1=Label(root, text="Hello world!")
myLabel2=Label(root, text="My name is ganesh")
myLabel3=Label(root, text="My name is siya")

myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=4)
myLabel3.grid(row=3, column=3)

root.mainloop()