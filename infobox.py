#!/usr/bin/python
# Info box 

import os
import sys
import time
import datetime

import Tkinter as tk
from Tkinter import *


# Main Window
root = tk.Tk(className = "Info")
root.geometry("256x276")
root.title("Info")
root.option_add("*Font", "TkDefaultFont 9")

# title
frame1 = Frame()
frame1.pack(fill=X)
        
label1 = Label(frame1, anchor=W, text="Title:", width=6)
label1.pack(side=LEFT, padx=4, pady=4)           
       
entry1 = Entry(frame1)
entry1.pack(fill=X, padx=4, expand=True)
        
# author
frame2 = Frame()
frame2.pack(fill=X)
        
label2 = Label(frame2, anchor=W, text="Author:", width=6)
label2.pack(side=LEFT, padx=4, pady=4)        

entry2 = Entry(frame2)
entry2.pack(fill=X, padx=4, expand=True)
   
# review     
frame3 = Frame()
frame3.pack(fill=BOTH, expand=True)
        
label3 = Label(frame3, anchor=W, text="Review:", width=6)
label3.pack(side=LEFT, anchor=N, padx=4, pady=4)        

txt = Text(frame3, height=10)
txt.pack(fill=BOTH, pady=4, padx=4, expand=True)


# buttons
clearButton = Button(text="Clear", command=lambda: txt.delete(1.0, END))
clearButton.pack(side='left', padx=64, pady=4)
            
closeButton = Button(text="Close", command=root.destroy)
closeButton.pack(side='right', padx=4, pady=4)

root.mainloop()  
