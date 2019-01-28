#!/usr/bin/python
# Texpert Text Editor 
# David Lawson 2018

import os
os.system('clear')
import time
import datetime
import platform

import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox

# main window
root = Tkinter.Tk(className = "Texpert")
texpert = ScrolledText(root, width=104, height=34, bg="white", undo=True)
root.option_add("*Font", "TkDefaultFont 9")


# Define Menu Functions
# file menu
def new_com(): 
    root.title("Untitled ") 
    file = None
    texpert.delete(1.0,END) 

def open_com():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select File')
    if file != None:
  	contents = file.read()
	texpert.insert('1.0', contents)
	file.close()

def saveas_com():
    file = tkFileDialog.asksaveasfile(mode='w')
    if file != None:
	data = texpert.get('1.0', END+'-1c')
	file.write(data)
 	file.close()

def close_com():
    root.title("") 
    file = None
    texpert.delete(1.0,END) 

def exit_com():
    if tkMessageBox.askokcancel("Exit", "Do you really want to exit? "):
	root.destroy()

# edit menu
def undo_com():
    texpert.edit_undo()

def redo_com():
    texpert.edit_redo()

def cut_com(): 
    texpert.event_generate("<<Cut>>")

def copy_com(): 
    texpert.event_generate("<<Copy>>") 

def paste_com(): 
    texpert.event_generate("<<Paste>>")  

def select_all():
    texpert.tag_add(SEL, "1.0", END)
    texpert.mark_set(INSERT, "1.0")
    texpert.see(INSERT)
    return 'break'
texpert.bind("<Control-Key-a>", select_all)
texpert.bind("<Control-Key-A>", select_all)

# view menu
def normal_com():
    root.attributes('-zoomed', False)

def full_com():
    root.attributes('-zoomed', True)

def panel_com():
    root.iconify()

# tools menu
def time_com():
    ctime = time.strftime('%I:%M:%p')
    texpert.insert(INSERT, ctime, "a")

def date_com():
    full_date = time.localtime()
    day = str(full_date.tm_mday)
    month = str(full_date.tm_mon)
    year = str(full_date.tm_year)
    date = ""+month+'/'+day+'/'+year
    texpert.insert(INSERT, date, "a")

# help menu
def about_com():
    label = tkMessageBox.showinfo("About", "Texpert\n\nA small text editor\ndesigned for linux.\n\nVersion 2.4 ")

def info_com():
    label = tkMessageBox.showinfo("Info", "Text Editor\n\nMade in Python\nwith Tkinter ")

def trouble_com():
    label = tkMessageBox.showinfo("Troubleshooting", "This program was designed for Linux and\nmay not work on other operating systems. \n\nTexpert text editor is a work in progress\nand is not yet complete.\n\nThe 'right click' menu is now working.\n\nThe 'Save' and 'Save As' options both work\nas 'save as'. This will be fixed (eventually).\n\n('>\n//)\n|\\ ")


# add menu/labels
menu = Menu(root, bd=1)
root.config(menu=menu, bd=1)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File ", menu=filemenu)
filemenu.add_command(label="New", command=new_com) 
filemenu.add_command(label="Open", command=open_com)
filemenu.add_separator()
filemenu.add_command(label="Save", command=saveas_com)
filemenu.add_command(label="Save As", command=saveas_com)
filemenu.add_separator()
filemenu.add_command(label="Close", command=close_com)
filemenu.add_command(label="Exit", command=exit_com)

editmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit ", menu=editmenu)
editmenu.add_command(label="Undo", command=undo_com)
editmenu.add_command(label="Redo", command=redo_com)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=cut_com)
editmenu.add_command(label="Copy", command=copy_com)  
editmenu.add_command(label="Paste", command=paste_com) 
editmenu.add_separator()
editmenu.add_command(label="Select All        Ctrl+a", command=select_all) 

viewmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="View ", menu=viewmenu)
viewmenu.add_command(label="Normal", command=normal_com)
viewmenu.add_command(label="Fullscreen", command=full_com)
viewmenu.add_separator()
viewmenu.add_command(label="Panel/Tray", command=panel_com)

toolmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Tools ", menu=toolmenu)
toolmenu.add_command(label="Insert Time", command=time_com)
toolmenu.add_command(label="Insert Date", command=date_com)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=helpmenu)
helpmenu.add_command(label="About", command=about_com)
helpmenu.add_command(label="Info", command=info_com)
helpmenu.add_command(label="Troubleshooting", command=trouble_com)


# right click menu
def r_click(event):
    editmenu.tk_popup(event.x_root, event.y_root)
texpert.bind("<Button-3>", r_click)

# x_out window
def x_out():
    if tkMessageBox.askokcancel("Exit", "Are you sure? "):
       root.destroy()


#toolBar
toolbar = Frame(root)
b = Button(toolbar, text="Open", width=4, command=open_com)
b.pack(side=LEFT, padx=4, pady=2)
b = Button(toolbar, text="Save", width=4, command=saveas_com)
b.pack(side=RIGHT, padx=4, pady=2)
toolbar.pack(side=TOP, fill=X)


#statusBar
status = Label(text="Simon says. Texpert does. You edit.", bd=1, relief=FLAT, anchor=W)
#status = Label(text="Linux + Python = Texpert", bd=1, relief=FLAT, anchor=W)
status.pack(side=BOTTOM, fill=Y)

texpert.pack(fill="both", expand=True)
root.title("Texpert")
texpert.focus_set()
root.protocol("WM_DELETE_WINDOW", x_out)
root.mainloop()
