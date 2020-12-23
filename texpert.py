#!/usr/bin/python
# Texpert Text Editor
# Written by David Lawson


import os
import sys
import time


try:
    import Tkinter as tk
    import ScrolledText as tkst
    import tkFileDialog
except:
    import tkinter as tk
    import tkinter.scrolledtext as tkst
    import tkinter.filedialog as tkFileDialog


#Mode Colors (mutable)
darkbg, darkfg, darkins = ("#181818", "#F5F5F5", "#F5F5F5")
lightbg, lightfg, lightins = ("#F5F5F5", "#181818", "#181818")
legalbg, legalfg, legalins = ("#FFFFCC", "#181818", "#181818")
nightbg, nightfg, nightins = ("#181818", "#00FF33", "#00FF33")


root = tk.Tk()
root.title("Texpert")
root.geometry("700x500")
root.option_add("*Font", "TkDefaultFont 9")
current_file = None


#Main Frame
mainframe = tk.Frame(root, bd=1, relief='flat')
mainframe.pack(fill='both', expand=True, padx=0, pady=0)

#Text Area
texpert = tkst.ScrolledText(mainframe, undo=True, bd=0, font=("Arial 11"))
texpert.pack(side='bottom', fill='both', expand=True)
texpert.config(padx=2, pady=2, wrap="word", bg=lightbg, fg=lightfg, 
                insertbackground=lightins)
texpert.focus_set()

#StatusBar
statusbar = tk.Frame(root, bd=1, relief='sunken')
statusbar.pack(side='bottom', fill='x')
mode = tk.Label(statusbar, text=" Mode: Light")
mode.pack(side='left')
line_lbl = tk.Label(statusbar, text="Line 1, Col 1")
line_lbl.pack(side='right', padx=10)


#Menu Functions
#file menu
def new_com(event=None):
    root.title("New Document - Texpert")
    file = None
    texpert.delete('1.0', 'end-1c')


def open_com(event=None):
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title="Select File", 
    filetypes = (("Text Files", "*.txt"),("All Files", "*.*")))
    if file:
        contents = file.read()
        name = root.title((file.name) + " - Texpert")
        texpert.delete('1.0', 'end-1c')
        texpert.insert('1.0', contents)
        file.close()
        global current_file
        current_file = file.name


def save_com(event=None):
    if current_file:
        file = open(current_file, "w")
        data = texpert.get('1.0', 'end-1c')
        file.write(data)
        file.close()
    else:
        saveas_com()


def saveas_com(event=None):
    file = tkFileDialog.asksaveasfile(mode='w', 
    filetypes = (("Text Files", "*.txt"),("All Files", "*.*")))
    if file:
        data = texpert.get('1.0', 'end-1c')
        file.write(data)
        file.close()
        global current_file
        current_file = file.name


#print/print preview not done
def print_com():
    print("Printer not found")


def preview_com():
    root.geometry("760x800+440+175")
    texpert.config(padx=30, pady=8, wrap="word", font=('Arial 10'))
    statusbar.pack_forget()
    toolbar.pack_forget()
    toolbar2.pack(side='top', anchor='n', fill='x')


def close_com(event=None):
    root.title("Untitled - Texpert")
    file = None
    texpert.delete('1.0', 'end-1c')


def exit_com(event=None):
    win = tk.Toplevel()
    win.title("Exit")
    xit = tk.Label(win, text="\nUnsaved work will be lost.\n\nAre you sure you want to exit?\n")
    xit.pack()
    ex = tk.Button(win, text="Exit", width=4, command=root.destroy)
    ex.pack(side='left', padx=24, pady=4)
    ex.focus_set()
    ex.bind("<Return>", (lambda event: root.destroy()))
    can = tk.Button(win, text="Cancel", width=4, command=win.destroy)
    can.pack(side='right', padx=24, pady=4)
    win.transient(root)
    win.geometry('240x120')
    win.wait_window()


#for print preview
def nine_font():
    texpert.config(font=('Arial 9'))

def tenn_font():
    texpert.config(font=('Arial 10'))

def levn_font():
    texpert.config(font=('Arial 11'))

def twev_font():
    texpert.config(font=('Arial 12'))

def fort_font():
    texpert.config(font=('Arial 14'))


#edit menu
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

def select_all(event=None):
    texpert.tag_add('sel', '1.0', 'end-1c')
    texpert.mark_set('insert', '1.0')
    texpert.see('insert')
    return 'break'


#view menu
def tool_bar():
    if is_toolbar.get():
        toolbar.pack_forget()
    else:
        toolbar.pack(side='top', anchor='n', fill='x')


def status_bar():
    if is_statusbar.get():
        statusbar.pack_forget()
    else:
        statusbar.pack(side='bottom', fill='x')


#modes for: [view > mode]
def dark_mode():
    mode["text"] = " Mode: Dark"
    texpert.config(bg=darkbg, fg=darkfg, insertbackground=darkins)
    tex.config(bg=darkbg, fg=darkfg, insertbackground=darkins)


def light_mode():
    mode["text"] = " Mode: Light"
    texpert.config(bg=lightbg, fg=lightfg, insertbackground=lightins)
    tex.config(bg=lightbg, fg=lightfg, insertbackground=lightins)
 
    
def legal_mode():
    mode["text"] = " Mode: Legal"
    texpert.config(bg=legalbg, fg=legalfg, insertbackground=legalins)
    tex.config(bg=legalbg, fg=legalfg, insertbackground=legalins)


def night_mode():
    mode["text"] = " Mode: Night"
    texpert.config(bg=nightbg, fg=nightfg, insertbackground=nightins)
    tex.config(bg=nightbg, fg=nightfg, insertbackground=nightins)


def transparent():
    if is_transparent.get():
        root.wm_attributes('-alpha', 0.9)
    else:
        root.wm_attributes('-alpha', 1.0)


def blockcursor():
    if is_blockcursor.get():
        texpert.config(padx=2, pady=2, wrap="word", blockcursor=True)
    else:
        texpert.config(padx=2, pady=2, wrap="word", blockcursor=False)


def tray_com():
    root.iconify()


def vertical_view():
    root.attributes('-zoomed', False)
    root.geometry("560x640+440+165")
    texpert.config(padx=2, pady=2, wrap="word", font=("Arial 11"))
    statusbar.pack(side='bottom', fill='x')
    toolbar.pack(side='top', anchor='n', fill='x')
    toolbar2.pack_forget()


def default_view(event=None):
    root.attributes('-zoomed', False)
    root.geometry("700x500+440+165")
    texpert.config(padx=2, pady=2, wrap="word", font=("Arial 11"))
    statusbar.pack(side='bottom', fill='x')
    toolbar.pack(side='top', anchor='n', fill='x')
    toolbar2.pack_forget()


def full_screen(event=None):
    root.attributes('-zoomed', True)
    texpert.config(padx=2, pady=2, wrap="word", font=("Arial 11"))
    statusbar.pack(side='bottom', fill='x')
    toolbar.pack(side='top', anchor='n', fill='x')
    toolbar2.pack_forget()


#tools menu
def time_com():
    ctime = time.strftime('%I:%M %p')
    texpert.insert('insert', ctime, "a", ' ')

def date_com():
    full_date = time.localtime()
    day = str(full_date.tm_mday)
    month = str(full_date.tm_mon)
    year = str(full_date.tm_year)
    date = "" + month + '/' + day + '/' + year
    texpert.insert('insert', date, "a", ' ')


def fname():
    texpert.insert('insert', current_file)


def note_area():
    if is_notearea.get():
        note_frame.pack(side='right', anchor='e', fill='y')
    else:
        note_frame.pack_forget()


#help menu
def about_com(event=None):
    win = tk.Toplevel()
    win.title("About")
    bout = tk.Label(win, text="""\n\n\nTexpert
    \nA small and lightweight text editor
    \nMade in Python with Tkinter\n\n""")
    bout.pack()
    cre = tk.Button(win, text="Credits", width=4, command=credits_com)
    cre.pack(side='left', padx=8, pady=4)
    clo = tk.Button(win, text="Close", width=4, command=win.destroy)
    clo.pack(side='right', padx=8, pady=4)
    win.transient(root)
    win.geometry('300x200+638+298')
    win.wait_window()


def credits_com():
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 0)
    win.title("Credits")
    cred = tk.Label(win, foreground="#404040",
                    text="""\n\n\nCreated by David Lawson
    \n\nme = Person()\nwhile (me.awake()):\nme.code()\n""")
    cred.pack()
    lic = tk.Button(win, text="License", width=4, command=license_info)
    lic.pack(side='left', padx=8, pady=4)
    cls = tk.Button(win, text="Close", width=4, command=win.destroy)
    cls.pack(side='right', padx=8, pady=4)
    win.transient(root)
    win.geometry('300x200+638+298')
    win.wait_window()


def license_info():
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 1)
    win.title("License")
    lic = tk.Label(win, justify='left', text="""\n\nMIT License

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
DEALINGS IN THE SOFTWARE.\n\n""")
    lic.pack()
    cls = tk.Button(win, text="Close", command=win.destroy)
    cls.pack()
    win.transient(root)
    win.geometry('480x450+550+230')
    win.wait_window()


def trouble_com(event=None):
    win = tk.Toplevel()
    win.title("Troubleshooting")
    trouble = tk.Label(win, justify='left', text="""\n\n
This program was designed for Linux and
may not work on other operating systems
(i.e., rendering and/or functionality issues).\n
Texpert text editor is a work in progress
and may or may not ever be completed.\n\n
Known Issues:\n 
Line/Col numbers are not fully functional.
Problem remains: unfixed.\n
Print preview is not entirely accurate.\n
Also, (pay attention because this is important)
anything typed in note area will not be saved
as it was not designed/programmed to do so.
\n\nAnyway..\n""")
    trouble.pack()
    cls = tk.Button(win, text="Close", command=win.destroy)
    cls.pack()
    win.transient(root)
    win.geometry('354x408+612+230')
    win.wait_window()


def shortcut_keys(event=None):
    win = tk.Toplevel()
    win.title("Shortcut Keys")
    shortk = tk.Label(win, justify='left',
                    text="""\n
List of shortcut keys and their functions.\n\n
Menu \tKeys\t\tFunctions\n  
File:\tCtrl+N   \t\tNew File
    \tCtrl+O    \t\tOpen File
    \tCtrl+S    \t\tSave File
    \tCtrl+Shift+S\tSave As
    \tCtrl+W    \t\tClose File
    \tCtrl+Q    \t\tQuit Program (exit)\n\n
Edit:\tCtrl+Z   \t\tUndo
    \tCtrl+Shift+Z\tRedo
    \tCtrl+X    \t\tCut
    \tCtrl+C    \t\tCopy
    \tCtrl+V    \t\tPaste
    \tCtrl+A    \t\tSelect All\n\n
View:\tCtrl+D   \t\tDefault Win Size
    \tF11       \t\tFullscreen
    \tEscape    \t\tExit Fullscreen
\n\n""")
    shortk.pack()
    cls = tk.Button(win, text="Close", command=win.destroy)
    cls.pack()
    win.transient(root)
    win.geometry('380x460+600+230')
    win.wait_window()


#context menu (right-click)
def r_click(event):
    editmenu.tk_popup(event.x_root, event.y_root)
texpert.bind("<Button-3>", r_click)

#line count (statusbar)
def linecount(event):
    (line, char) = map(int, event.widget.index("end-1c").split("."))
    line_lbl['text'] = 'Line {line}, Col {col}'.format(line=line, col=char + 1)
texpert.bind("<KeyRelease>", linecount)



#Main Menu
menu = tk.Menu(root, bd=1, relief='flat')
root.config(menu=menu, bd=2)

#File
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File ", menu=filemenu)
filemenu.add_command(label="New", 
                    command=new_com,
                    accelerator="Ctrl+N".rjust(15))
filemenu.add_command(label="Open", 
                    command=open_com,
                    accelerator="Ctrl+O".rjust(15))
filemenu.add_separator()
filemenu.add_command(label="Save", 
                    command=save_com,
                    accelerator="Ctrl+S".rjust(15))
filemenu.add_command(label="Save As", 
                    command=saveas_com,
                    accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Print", 
                    command=print_com, state="disabled")
filemenu.add_command(label="Print Preview", 
                    command=preview_com)
filemenu.add_separator()
filemenu.add_command(label="Close", 
                    command=close_com,
                    accelerator="Ctrl+W".rjust(15))
filemenu.add_command(label="Exit", 
                    command=exit_com, underline=1,
                    accelerator="Ctrl+Q".rjust(15))

#Edit
editmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit ", menu=editmenu)
editmenu.add_command(label="Undo", 
                    command=undo_com,
                    accelerator="Ctrl+Z".rjust(15))
editmenu.add_command(label="Redo", 
                    command=redo_com,
                    accelerator="Ctrl+Shift+Z")
editmenu.add_separator()
editmenu.add_command(label="Cut", 
                    command=cut_com,
                    accelerator="Ctrl+X".rjust(15))
editmenu.add_command(label="Copy", 
                    command=copy_com,
                    accelerator="Ctrl+C".rjust(15))
editmenu.add_command(label="Paste", 
                    command=paste_com,
                    accelerator="Ctrl+V".rjust(15))
editmenu.add_separator()
editmenu.add_command(label="Select All", 
                    command=select_all,
                    accelerator="Ctrl+A".rjust(15))


#View
viewmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View ", menu=viewmenu)
is_toolbar = tk.BooleanVar()
is_toolbar.trace('w', lambda *args: tool_bar())
viewmenu.add_checkbutton(label="Toolbar",
                        variable=is_toolbar,
                        onvalue=0,
                        offvalue=1)
is_statusbar = tk.BooleanVar()
is_statusbar.trace('w', lambda *args: status_bar())
viewmenu.add_checkbutton(label="Statusbar",
                        variable=is_statusbar,
                        onvalue=0,
                        offvalue=1)
viewmenu.add_separator()

#sub-menu buttons for: [view > mode]
submenu = tk.Menu(menu, tearoff=0)
viewmenu.add_cascade(label="Mode ", menu=submenu)
submenu.add_command(label=" Dark ", 
                    command=dark_mode,
                    activebackground=darkbg,
                    activeforeground=darkfg)
submenu.add_command(label=" Light ", 
                    command=light_mode,
                    activebackground=lightbg,
                    activeforeground=lightfg)
submenu.add_command(label=" Legal ", 
                    command=legal_mode,
                    activebackground=legalbg,
                    activeforeground=legalfg)
submenu.add_command(label=" Night ", 
                    command=night_mode,
                    activebackground=nightbg,
                    activeforeground=nightfg)

is_transparent = tk.BooleanVar()
is_transparent.trace('w', lambda *args: transparent())
viewmenu.add_checkbutton(label="Transparency",
                        variable=is_transparent,
                        onvalue=1,
                        offvalue=0)
is_blockcursor = tk.BooleanVar()

is_blockcursor.trace('w', lambda *args: blockcursor())
viewmenu.add_checkbutton(label="Block Cursor",
                        variable=is_blockcursor,
                        onvalue=1,
                        offvalue=0)

viewmenu.add_separator()
viewmenu.add_command(label="Hide in Tray", command=tray_com)
viewmenu.add_separator()
viewmenu.add_command(label="Vertical", command=vertical_view)
viewmenu.add_command(label="Default", command=default_view,
                    accelerator="Ctrl+D")
viewmenu.add_command(label="Fullscreen", command=full_screen,
                    accelerator="F11".rjust(8))


#Tools
toolmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tools ", menu=toolmenu)
toolmenu.add_command(label="Insert Time", command=time_com)
toolmenu.add_command(label="Insert Date", command=date_com)
toolmenu.add_command(label="Insert Path/File", command=fname)
is_notearea = tk.BooleanVar()
is_notearea.trace('w', lambda *args: note_area())
toolmenu.add_checkbutton(label="Note Area", variable=is_notearea)


#Help
helpmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=helpmenu)
helpmenu.add_command(label="About", command=about_com)
helpmenu.add_command(label="Troubleshooting", command=trouble_com)
helpmenu.add_command(label="Shortcut Keys", command=shortcut_keys)


#ToolBar (main)
toolbar = tk.Frame(mainframe, bd=2, relief='groove')
toolbar.pack(side='top', anchor='n', fill='x')
b1 = tk.Button(toolbar, text="Open", width=5, command=open_com)
b1.pack(side='left', padx=4, pady=2)
b2 = tk.Button(toolbar, text="Save", width=5, command=save_com)
b2.pack(side='right', padx=4, pady=2)
b4 = tk.Button(toolbar, text="Notes", width=5,
                command=lambda: is_notearea.set(not is_notearea.get()))
b4.pack(side='right', padx=4, pady=2)

#ToolBar 'Mode' button
var = tk.StringVar(toolbar)
var.set("Mode")
w = tk.OptionMenu(toolbar, variable=var, value='')
w.config(indicatoron=0, bd=1, width=7, padx=4, pady=5)
w.pack(side='left', padx=4, pady=2)
first = tk.BooleanVar()
second = tk.BooleanVar()
third = tk.BooleanVar()
fourth = tk.BooleanVar()
w['menu'].delete('0', 'end')
w['menu'].add_checkbutton(label=" Dark  ", onvalue=1, offvalue=0,
                            activebackground=darkbg,
                            activeforeground=darkfg,
                            variable=first,
                            command=dark_mode,
                            indicatoron=0)
w['menu'].add_checkbutton(label=" Light  ", onvalue=1, offvalue=0,
                            activebackground=lightbg,
                            activeforeground=lightfg,
                            variable=second,
                            command=light_mode,
                            indicatoron=0)
w['menu'].add_checkbutton(label=" Legal  ", onvalue=1, offvalue=0,
                            activebackground=legalbg,
                            activeforeground=legalfg,
                            variable=third,
                            command=legal_mode,
                            indicatoron=0)
w['menu'].add_checkbutton(label=" Night  ", onvalue=1, offvalue=0,
                            activebackground=nightbg,
                            activeforeground=nightfg,
                            variable=fourth,
                            command=night_mode,
                            indicatoron=0)


#Toolbar2 (for print preview)
toolbar2 = tk.Frame(mainframe, bd=2, relief='groove')
b2 = tk.Button(toolbar2, text="Close Preview", width=10, command=default_view)
b2.pack(side='right', padx=28, pady=4)

#Toolbar2 'Zoom' button
var = tk.StringVar()
var.set("Zoom Level")
w2 = tk.OptionMenu(toolbar2, variable=var, value='')
w2.config(indicatoron=0, bd=1, width=12, padx=4, pady=5)
w2.pack(side='left', padx=28, pady=4)
one = tk.BooleanVar()
two = tk.BooleanVar()
three = tk.BooleanVar()
four = tk.BooleanVar()
five = tk.BooleanVar()
w2['menu'].delete('0', 'end')
w2['menu'].add_radiobutton(label=" 60% ".rjust(6), variable="", value=1, command=nine_font)
w2['menu'].add_radiobutton(label=" 75% ".rjust(6), variable="", value=2, command=tenn_font)
w2['menu'].add_radiobutton(label="100% ", variable="", value=3, command=levn_font)
w2['menu'].add_radiobutton(label="125% ", variable="", value=4, command=twev_font)
w2['menu'].add_radiobutton(label="150% ", variable="", value=5, command=fort_font)


#Init Note Area
note_frame = tk.Frame(texpert, bd=0, relief='sunken')
tex = tk.Text(note_frame, width=18, undo=True)
tex.pack(side='top', fill='both', expand=True)
tex.config(padx=2, pady=2, wrap="word", bg=lightbg, fg=lightfg)
tex.insert('1.0', "Notes are not saved..")
clear = tk.Button(note_frame, text="Clear", width=4,
                    command=lambda: tex.delete('1.0', 'end-1c'))
clear.pack(side='left', padx=2, pady=2)
close = tk.Button(note_frame, text="Close", width=4,
                    command=lambda: is_notearea.set(not is_notearea.get()))
close.pack(side='right', padx=2, pady=2)


#bindings
root.bind_all('<Control-a>', select_all)
root.bind_all('<Control-n>', new_com)
root.bind_all('<Control-o>', open_com)
root.bind_all('<Control-s>', save_com)
root.bind_all("<Control-Shift-S>", saveas_com)
root.bind_all('<Control-w>', close_com)
root.bind_all('<Control-q>', exit_com)
root.bind_all('<Control-d>', default_view)
root.bind_all('<F11>', full_screen)
root.bind("<Escape>", lambda event: root.attributes("-zoomed", False))


root.protocol("WM_DELETE_WINDOW", exit_com)
root.mainloop()
