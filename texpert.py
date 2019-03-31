#!/usr/bin/python
# Texpert Text Editor 
# Written by David Lawson

import os
import sys
import time
import datetime

import Tkinter as tk
#from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import ttk


class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


# Main
root = tk.Tk(className = "Texpert")
root.geometry("700x454")
root.title("Texpert")
texpert = ScrolledText(root, padx=2, pady=2, undo=True, font=('Arial 11'))
texpert.config(wrap="word")
root.option_add("*Font", "TkDefaultFont 9")


# Menu Functions
# file menu
def new_com(): 
    root.title("Untitled ") 
    file = None
    texpert.delete('1.0', 'end-1c') 
    
def open_com():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select File')
    if file is not None:
  	contents = file.read()
        texpert.delete('1.0', 'end-1c')
	texpert.insert('1.0', contents)
	file.close()

def save_com():
    print ("Silent Save")

def saveas_com():
    file = tkFileDialog.asksaveasfile(mode='w')
    if file is not None:
	data = texpert.get('1.0', 'end-1c')
	file.write(data)
 	file.close()

def close_com():
    root.title('') 
    file = None
    texpert.delete('1.0', 'end-1c') 
    
def exit_com():
    if tkMessageBox.askokcancel("Exit", "Do you really want to exit?"):
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
    texpert.tag_add('sel', '1.0', 'end-1c')
    texpert.mark_set('insert', '1.0')
    texpert.see('insert')
    return 'break'
texpert.bind("<Control-Key-a>", select_all)
texpert.bind("<Control-Key-A>", select_all)

# view menu
def hide_toolbar():
    toolbar.pack_forget()

def show_toolbar():
    toolbar.pack(side='top', fill='x')

#sub-menu for: [view > mode]
def dark_mode():
    global status
    status["text"] = " Mode: Dark"
    texpert.config(background="#181818", fg="#F5F5F5", insertbackground="#F5F5F5")

def light_mode():
    global status
    status["text"] = " Mode: Light"
    texpert.config(background="#F5F5F5", fg="#181818", insertbackground="#181818")

def legal_mode():
    global status
    status["text"] = " Mode: Legal Pad"
    texpert.config(background="#FFFFCC", fg="#181818", insertbackground="#181818")

def night_mode():
    global status
    status["text"] = " Mode: Night Vision"
    texpert.config(background="#181818", fg="#00FF33", insertbackground="#00FF33")

def desert_mode():
    global status
    status["text"] = " Mode: Desert View"
    texpert.config(background="#E9DDB3", fg="#40210D", insertbackground="#40210D")

def mint_mode():
    global status
    status["text"] = " Mode: Chocolate Mint"
    texpert.config(background="#CCFFCC", fg="#40210D", insertbackground="#40210D")

def tray_com():
    root.iconify()

def slim_view():
    root.attributes('-zoomed', False)
    root.geometry("540x600+440+188")
    texpert = ScrolledText(root, padx=2, pady=2, undo=True, font=('Arial 11'))
    texpert.config(wrap="word")
    root.option_add("*Font", "TkDefaultFont 9")

def default_view():
    root.attributes('-zoomed', False)
    root.geometry("700x454+440+188") #size+position
    texpert = ScrolledText(root, padx=2, pady=2, undo=True, font=('Arial 11'))
    texpert.config(wrap="word")
    root.option_add("*Font", "TkDefaultFont 9")

def full_screen():
    root.attributes('-zoomed', True)

# tools menu
def time_com():
    ctime = time.strftime('%I:%M %p')
    texpert.insert('insert', ctime, "a")

def date_com():
    full_date = time.localtime()
    day = str(full_date.tm_mday)
    month = str(full_date.tm_mon)
    year = str(full_date.tm_year)
    date = ""+month+'/'+day+'/'+year
    texpert.insert('insert', date, "a")

def note_area():
    if is_notearea.get():
        note.pack(side='right', fill='y', padx=0, pady=0)
        btn_frame.pack(side='bottom', fill='y', padx=0, pady=0)
    else:
        note.pack_forget()
        btn_frame.pack_forget()


# help menu
def about_com():
    win = tk.Toplevel()
    win.title("About")                                     
    tk.Label(win, text="\n\n\nTexpert\n\nA small text editor designed for Linux\n\nMade in Python with Tkinter\n\n\n").pack()   
    
    a = tk.Button(win, text="Credits", width=4, command=credits_com)
    a.pack(side='left', padx=8, pady=4)
    ver = tk.Label(win, text="v 1.0", width=4, bd=0, state='disabled')
    ver.pack(side='left', padx=8, pady=4, expand='yes')
    b = tk.Button(win, text="Close", width=4, command=win.destroy)
    b.pack(side='right', padx=8, pady=4)
     
    win.transient(root)
    win.geometry('300x200')
    win.wait_window()

def credits_com(): 
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 0)
    win.title("Credits")                                     
    tk.Label(win, foreground="#404040", text="\n\n\nCreated by David Lawson\n\n\nme = Person()\nwhile (me.awake()):\nme.code()\n\n").pack()   
    
    a = tk.Button(win, text="License", width=4, command=license_info)
    a.pack(side='left', padx=8, pady=4)
    b = tk.Button(win, text="Close", width=4, command=win.destroy)
    b.pack(side='right', padx=8, pady=4) 
    
    win.transient(root)
    win.geometry('300x200')
    win.wait_window()

def license_info():
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 1)
    win.title("License")                                     
    tk.Label(win, justify='left', text="""\n\nMIT License

Copyright (c) 2019 David Lawson

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.\n\n""").pack()   
    
    tk.Button(win, text='Close', command=win.destroy).pack()   
    win.transient(root)
    win.geometry('480x449')
    win.wait_window()


def trouble_com():
    win = tk.Toplevel()
    win.title("Troubleshooting")                                     
    tk.Label(win, justify='left', text="\n\nThis program was designed for Linux and\nmay not work on other operating systems. \n\nTexpert text editor is a work in progress\nand will probably never be complete.\n\n\n\nKnown Issues:\n\n'Show toolbar' is temporarily disabled\nbecause the toolbar refuses to remember\nits original position. I may or may not\nmake an attempt to fix this someday.\n\nThe 'Save' and 'Save As' options both work\nas 'save as'. This should be fixed someday.\n\n").pack()   
    tk.Button(win, text='Close', command=win.destroy).pack()   
    win.transient(root)
    win.geometry('350x350')
    win.wait_window()


# Menu Buttons/Labels
menu = tk.Menu(root, bd=1, relief='flat')
root.config(menu=menu, bd=2)

#file menu
filemenu = tk.Menu(menu, tearoff=0)
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
editmenu = tk.Menu(menu, tearoff=0)
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
viewmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View ", menu=viewmenu)
viewmenu.add_command(label="Hide Toolbar", command=hide_toolbar)
viewmenu.add_command(label="Show Toolbar", command=show_toolbar, state='disabled')
viewmenu.add_separator()

#sub-menu for: [view > mode]
submenu = tk.Menu(menu, tearoff=0)
viewmenu.add_cascade(label="Mode ", menu=submenu)
submenu.add_command(label=" Dark", command=dark_mode, activebackground="#181818", activeforeground="#F5F5F5")
submenu.add_command(label=" Light", command=light_mode, activebackground="#F5F5F5", activeforeground="#181818")
submenu.add_command(label=" Legal Pad", command=legal_mode, activebackground="#FFFFCC", activeforeground="#181818")
submenu.add_command(label=" Night Vision", command=night_mode, activebackground="#181818", activeforeground="#00FF33")
submenu.add_command(label=" Desert View", command=desert_mode, activebackground="#E9DDB3", activeforeground="#40210D")
submenu.add_command(label=" Chocolate Mint", command=mint_mode, activebackground="#CCFFCC", activeforeground="#40210D")

viewmenu.add_separator()
viewmenu.add_command(label="Hide in Tray", command=tray_com)
viewmenu.add_separator()
viewmenu.add_command(label="Slim View", command=slim_view)
viewmenu.add_command(label="Default", command=default_view)
viewmenu.add_command(label="Fullscreen", command=full_screen)

#tool menu
toolmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tools ", menu=toolmenu)
toolmenu.add_command(label="Insert Time", command=time_com)
toolmenu.add_command(label="Insert Date", command=date_com)
is_notearea = tk.BooleanVar()
is_notearea.trace('w', lambda *args: note_area())
toolmenu.add_checkbutton(label="Note Area", variable=is_notearea, indicatoron=1)

#help menu
helpmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=helpmenu)
helpmenu.add_command(label="About", command=about_com)
helpmenu.add_command(label="Troubleshooting", command=trouble_com)



# Context Menu (right-click)
def r_click(event):
    editmenu.tk_popup(event.x_root, event.y_root)
texpert.bind("<Button-3>", r_click)


# Toolbar/Buttons 
toolbar = tk.Frame(root, bd=2, relief='groove')
b1 = tk.Button(toolbar, text="Open", width=4, command=open_com)
b1.pack(side='left', padx=4, pady=2)
b2 = tk.Button(toolbar, text="Save", width=4, command=saveas_com)
b2.pack(side='right', padx=4, pady=2)
b4 = tk.Button(toolbar, text="Notes", width=4, 
            command=lambda: is_notearea.set(not is_notearea.get()))
b4.pack(side='right', padx=4, pady=2)
toolbar.pack(side='top', fill='x')


# Mode button (on toolbar)
var = tk.StringVar(root)
var.set("Mode")
w = tk.OptionMenu(toolbar, variable = var, value='')
w.config(indicatoron=0, bd=1, width=6, padx=4, pady=5)
w.pack(side='left', padx=4, pady=2)
first = tk.BooleanVar()
second = tk.BooleanVar()
third = tk.BooleanVar()
forth = tk.BooleanVar()
fifth = tk.BooleanVar()
sixth = tk.BooleanVar()
w['menu'].delete('0', 'end')
w['menu'].add_checkbutton(label="Dark", onvalue=1, offvalue=0, 
                         activebackground="#181818", activeforeground="#F5F5F5", 
                         variable=first, command=dark_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Light", onvalue=1, offvalue=0,
                         activebackground="#F5F5F5", activeforeground="#181818", 
                         variable=second, command=light_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Legal Pad", onvalue=1, offvalue=0,
                         activebackground="#FFFFCC", activeforeground="#181818", 
                         variable=third, command=legal_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Night Vision", onvalue=1, offvalue=0,
                         activebackground="#181818", activeforeground="#00FF33", 
                         variable=forth, command=night_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Desert View", onvalue=1, offvalue=0,
                         activebackground="#E9DDB3", activeforeground="#40210D", 
                         variable=fifth, command=desert_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Chocolate Mint", onvalue=1, offvalue=0,
                         activebackground="#CCFFCC", activeforeground="#40210D", 
                         variable=sixth, command=mint_mode, indicatoron=0)


# Init Note Area
btn_frame = tk.Frame()
note = tk.LabelFrame(texpert, bd=1, relief='ridge')
tx = tk.Text(note, width=18, bd=0, relief='flat', padx=0, pady=0)
tx.insert('1.0', "Nothing here is saved..")
tx.config(wrap="word")
tx.pack(side='top', fill='both', expand=True)
a = tk.Button(note, text="Clear", width=4, command=lambda: tx.delete('1.0', 'end-1c'))
a.pack(side='left', anchor='s', padx=2, pady=4)
b = tk.Button(note, text="Close", width=4, command=lambda: is_notearea.set(not is_notearea.get()))
b.pack(side='right', anchor='s', padx=2, pady=4)


# Black out checkbox
index = 0
def black_out():
    global index
    if index:
        status.config(bg="#D3D3D3", fg="#181818")
        toolbar.config(bg="#D3D3D3")
    else:
        status.config(bg="#181818", fg="#F5F5F5")
        toolbar.config(bg="#181818")
    index = not index


# statusBar
status = tk.Label(text=" Mode: Light", anchor='w', bd=1, relief='sunken', font=('Arial 10'))
b = tk.Checkbutton(status, text=" Black Out ", width=10, command=black_out, font=('Arial 10'))
b.pack(side='right', fill='x')
status.pack(side='bottom', fill='x')


# x_out window
def x_out():
    if tkMessageBox.askokcancel("Exit", "Unsaved work will be lost.\n\nAre you sure? "):
       root.destroy()


texpert.pack(fill='both', expand=True)
texpert.focus_set()
root.protocol("WM_DELETE_WINDOW", x_out)

if __name__ == "__main__":
    MainApp(root).pack(side="top")

root.mainloop()
