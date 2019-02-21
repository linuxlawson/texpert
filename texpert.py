#!/usr/bin/python
# Texpert Text Editor 
# David Lawson 2018

import os
import sys
import time
import datetime

import Tkinter as tk
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox


# Main Window
root = tk.Tk(className = "Texpert")
root.geometry("700x440")
root.title("Texpert")
texpert = ScrolledText(root, bg="white", undo=True, font=("Arial", 11))
root.option_add("*Font", "TkDefaultFont 9")


# Menu Functions
# file menu
def new_com(): 
    root.title("Untitled ") 
    file = None
    texpert.delete(1.0, 'end-1c') 
    
def open_com():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select File')
    if file is not None:
  	contents = file.read()
        texpert.delete(1.0, 'end-1c')
	texpert.insert('1.0', contents)
	file.close()

def save_com():
    print ("No")

def saveas_com():
    file = tkFileDialog.asksaveasfile(mode='w')
    if file is not None:
	data = texpert.get('1.0', 'end-1c')
	file.write(data)
 	file.close()

def close_com():
    root.title('') 
    file = None
    texpert.delete(1.0, 'end-1c') 
    
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
    texpert.tag_add(SEL, '1.0', 'end-1c')
    texpert.mark_set(INSERT, '1.0')
    texpert.see(INSERT)
    return 'break'
texpert.bind("<Control-Key-a>", select_all)
texpert.bind("<Control-Key-A>", select_all)

# view menu
def hide_tbar():
    toolbar.pack_forget()

def show_tbar():
    toolbar.pack(side=TOP, fill=X)

#sub-menu for: [view > mode]
def dark_mode():
    global status
    status["text"] = " Mode: Dark"
    texpert.config(background='#181818', fg='#F5F5F5', insertbackground='#F5F5F5')

def light_mode():
    global status
    status["text"] = " Mode: Light"
    texpert.config(background='white', fg='black', insertbackground='black')

def legal_mode():
    global status
    status["text"] = " Mode: Legal Pad"
    texpert.config(background='#FFFFCC', fg='black', insertbackground='black')

def green_mode():
    global status
    status["text"] = " Mode: Night Vision"
    texpert.config(background='#181818', fg='#00FF33', insertbackground='#00FF33')


def tray_com():
    root.iconify()

def normal_com():
    root.attributes('-zoomed', False)
    root.geometry("700x440+440+195") #window size,position

def full_com():
    root.attributes('-zoomed', True)

# tools menu
def time_com():
    ctime = time.strftime('%I:%M %p')
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
    win = Toplevel()
    win.title("About")                                     
    Label(win, foreground='black', text="\n\n\nTexpert\n\nA small text editor designed for Linux.\n\nMade in Python with Tkinter\n\n\n").pack()   
    
    a = Button(win, text="Credits", width=4, command=credits_com)
    a.pack(side=LEFT, padx=8, pady=4)
    b = Button(win, text="Close", width=4, command=win.destroy)
    b.pack(side=RIGHT, padx=8, pady=4)
     
    win.transient(root)
    win.geometry('300x200')
    win.wait_window()

def credits_com(): #linked to: [about > credits]
    win = Toplevel(background = '#606060')
    win.wm_attributes("-topmost", 1)
    win.title("Credits")                                     
    Label(win, foreground='#F5F5F5', background = '#606060', text="\n\n\nCreated by David Lawson\n\n\nme = Person()\nwhile (me.awake()):\nme.code()\n\n").pack()   
    Button(win, text='Close', bd=2, relief='groove', command=win.destroy).pack()   
    win.transient(root)
    win.geometry('300x200')
    win.wait_window()

def trouble_com():
    win = Toplevel()
    win.title("Troubleshooting")                                     
    Label(win, foreground='black', text="\n\nThis program was designed for Linux and\nmay not work on other operating systems. \n\nTexpert text editor is a work in progress\nand is not yet complete.\n\n'Show toolbar' is disabled because it\ndoes not remember original position.\nWill re-write some day.\n\nThe 'Save' and 'Save As' options both work\nas 'save as'. This will be fixed (eventually).\n\n").pack()   
    Button(win, text='Close', command=win.destroy).pack()   
    win.transient(root)
    win.geometry('300x268')
    win.wait_window()



# Menu Buttons/Labels
menu = Menu(root, bd=1, relief='flat')
root.config(menu=menu, bd=1)

#file menu
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File ", menu=filemenu)
filemenu.add_command(label="New", command=new_com) 
filemenu.add_command(label="Open", command=open_com)
filemenu.add_separator()
filemenu.add_command(label="Save", command=saveas_com)
filemenu.add_command(label="Save As", command=saveas_com)
filemenu.add_separator()
filemenu.add_command(label="Close", command=close_com)
filemenu.add_command(label="Exit", command=exit_com, underline=1)

#edit menu
editmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit ", menu=editmenu)
editmenu.add_command(label="Undo", command=undo_com)
editmenu.add_command(label="Redo", command=redo_com)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=cut_com)
editmenu.add_command(label="Copy", command=copy_com)  
editmenu.add_command(label="Paste", command=paste_com) 
editmenu.add_separator()
editmenu.add_command(label="Select All", command=select_all) 

#view menu
viewmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="View ", menu=viewmenu)
viewmenu.add_command(label="Hide Toolbar", command=hide_tbar)
viewmenu.add_command(label="Show Toolbar", command=show_tbar, state='disabled')
viewmenu.add_separator()

#sub-menu for: [view > mode]
submenu = Menu(menu, tearoff=0)
viewmenu.add_cascade(label="Mode ", menu=submenu)
submenu.add_command(label=" Dark", command=dark_mode, activebackground="#181818", activeforeground="#F5F5F5")
submenu.add_command(label=" Light", command=light_mode)
submenu.add_command(label=" Legal Pad", command=legal_mode, activebackground="#FFFFCC", activeforeground="black")
submenu.add_command(label=" Night Vision", command=green_mode, activebackground="#181818", activeforeground="#00FF33")

viewmenu.add_separator()
viewmenu.add_command(label="Hide in Tray", command=tray_com)
viewmenu.add_command(label="Normal", command=normal_com)
viewmenu.add_command(label="Fullscreen", command=full_com)

#tool menu
toolmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Tools ", menu=toolmenu)
toolmenu.add_command(label="Insert Time", command=time_com)
toolmenu.add_command(label="Insert Date", command=date_com)

#help menu
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=helpmenu)
helpmenu.add_command(label="About", command=about_com)
helpmenu.add_command(label="Troubleshooting", command=trouble_com)


# right click menu
def r_click(event):
    editmenu.tk_popup(event.x_root, event.y_root)
texpert.bind("<Button-3>", r_click)

# toolBar
toolbar = Frame(root, bd=2, relief='groove')
b1 = Button(toolbar, text="Open", width=4, command=open_com)
b1.pack(side=LEFT, padx=4, pady=2)

b2 = Button(toolbar, text="Save", width=4, command=saveas_com)
b2.pack(side=RIGHT, padx=4, pady=2)
toolbar.pack(side=TOP, fill=X)

# statusBar
status = Label(text=" Mode: Light", anchor=W, bd=1, relief='sunken', fg='#000000', font=("Arial", 10))
status.pack(side=BOTTOM, fill=X)

# x_out window
def x_out():
    if tkMessageBox.askokcancel("Exit", "Are you sure? "):
       root.destroy()


texpert.pack(fill="both", expand=True)
texpert.focus_set()
root.protocol("WM_DELETE_WINDOW", x_out)
root.mainloop()
