import tkinter as tk
import os
import f
import security
import banana


    

def write_slogan():
    os.system('python f.py')
    os.system('python security.py')
    os.system('python banana.py')

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
button.pack(side=tk.LEFT)
slogan = tk.Button(frame,
                   text="Knock Knock",
                   command=write_slogan)
slogan.pack(side=tk.LEFT)

root.mainloop()