#!/usr/bin/python
# Info box

import os
import sys
import time
import datetime
try:
    import Tkinter as tk
except:
    import tkinter as tk


class infobox:
    def __init__(self, master):
        self.master = master

        self.frame1 = tk.Frame()
        self.frame1.pack(fill=tk.X)

        self.label1 = tk.Label(self.frame1, anchor=tk.W, text="Title:", width=6)
        self.label1.pack(side=tk.LEFT, padx=4, pady=4)

        self.entry1 = tk.Entry(self.frame1)
        self.entry1.pack(fill=tk.X, padx=4, expand=True)

        # author
        self.frame2 = tk.Frame()
        self.frame2.pack(fill=tk.X)

        self.label2 = tk.Label(self.frame2, anchor=tk.W, text="Author:", width=6)
        self.label2.pack(side=tk.LEFT, padx=4, pady=4)

        self.entry2 = tk.Entry(self.frame2)
        self.entry2.pack(fill=tk.X, padx=4, expand=True)

        # review
        self.frame3 = tk.Frame()
        self.frame3.pack(fill=BOTH, expand=True)

        self.label3 = Label(self.frame3, anchor=tk.W, text="Review:", width=6)
        self.label3.pack(side=tk.LEFT, anchor=tk.N, padx=4, pady=4)

        self.txt = Text(self.frame3, height=10)
        self.txt.pack(fill=tk.BOTH, pady=4, padx=4, expand=True)


        # buttons
        self.clearButton = tk.Button(text="Clear", command=lambda: self.txt.delete(1.0, tk.END))
        self.clearButton.pack(side='left', padx=64, pady=4)


        self.closeButton = tk.Button(text="Close", command=self.master.destroy)
        self.closeButton.pack(side='right', padx=4, pady=4)

def main():
    root = tk.Tk(className = "Info")
    root.geometry("256x276")
    root.title("Info")
    root.option_add("*Font", "TkDefaultFont 9")
    root.mainloop()

if __name__ == '__main__':
    main()
