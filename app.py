import sys
import os
from tkinter import *

window=Tk()

window.title("Running Python Script")
window.geometry('550x200')
lbl = Label(window, text="Load products to google sheets")
lbl.grid(column=0, row=0)
def run():
    os.system('python ApisToDrive.py')

btn = Button(window, text="Load Products", bg="black", fg="white",command=run)
btn.grid(column=2, row=3)

window.mainloop()