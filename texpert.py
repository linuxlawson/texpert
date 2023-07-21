#!/usr/bin/python3
# Texpert Text Editor
# David Lawson

import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.filedialog as tkFileDialog
import time

root = tk.Tk()
root.title("Texpert")
root.geometry("700x506")
root.option_add("*Font", "TkDefaultFont 9")
current_file = None

#Mode Colors 
darkbg, darkfg, darkins = ("#181818", "#F5F5F5", "#F5F5F5")
lightbg, lightfg, lightins = ("#F5F5F5", "#181818", "#181818")
legalbg, legalfg, legalins = ("#FFFFCC", "#181818", "#181818")
nightbg, nightfg, nightins = ("#181818", "#00FF33", "#00FF33")

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

stat_date = time.strftime('%-m/%d/%Y')
stat_date = tk.Label(statusbar, text=stat_date)
stat_date.pack(side='right', padx=10)


#Menu Functions
#file menu
def new_com(event=None):
    root.title("New Document - Texpert")
    f = None
    texpert.delete('1.0', 'end-1c')


def open_com(event=None):
    f = tkFileDialog.askopenfile(parent=root, mode='rb', title="Select File", 
    filetypes = (("Text Files", "*.txt"),("All Files", "*.*")))
    if f:
        contents = f.read()
        name = root.title((f.name) + " - Texpert")
        texpert.delete('1.0', 'end-1c')
        texpert.insert('1.0', contents)
        f.close()
        global current_file
        current_file = f.name


def save_com(event=None):
    if current_file:
        f = open(current_file, "w")
        data = texpert.get('1.0', 'end-1c')
        f.write(data)
        f.close()
    else:
        saveas_com()


def saveas_com(event=None):
    f = tkFileDialog.asksaveasfile(mode='w', 
    filetypes = (("Text Files", "*.txt"),("All Files", "*.*")))
    if f:
        data = texpert.get('1.0', 'end-1c')
        f.write(data)
        f.close()
        global current_file
        current_file = f.name


#print/print preview 
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
    f = None
    texpert.delete('1.0', 'end-1c')


def exit_com(event=None):
    win = tk.Toplevel()
    win.title("Exit")
    xit = tk.Label(win, 
    text="\nUnsaved work will be lost.\n\nAre you sure you want to exit?\n")
    xit.pack()
    ex = tk.Button(win, text="Exit", width=4, command=root.destroy)
    ex.pack(side='left', padx=24, pady=4)
    ex.focus_set()
    ex.bind("<Return>", (lambda event: root.destroy()))
    can = tk.Button(win, text="Cancel", width=4, command=win.destroy)
    can.pack(side='right', padx=24, pady=4)
    win.transient(root)
    win.geometry('240x150')
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
#config makes note area color match
def dark_mode():
    mode["text"] = " Mode: Dark"
    texpert.config(bg=darkbg, fg=darkfg, insertbackground=darkins)
    #tex.config(bg=darkbg, fg=darkfg, insertbackground=darkins)


def light_mode():
    mode["text"] = " Mode: Light"
    texpert.config(bg=lightbg, fg=lightfg, insertbackground=lightins)
    #tex.config(bg=lightbg, fg=lightfg, insertbackground=lightins)
 
    
def legal_mode():
    mode["text"] = " Mode: Legal"
    texpert.config(bg=legalbg, fg=legalfg, insertbackground=legalins)
    #tex.config(bg=legalbg, fg=legalfg, insertbackground=legalins)


def night_mode():
    mode["text"] = " Mode: Night"
    texpert.config(bg=nightbg, fg=nightfg, insertbackground=nightins)
    #tex.config(bg=nightbg, fg=nightfg, insertbackground=nightins)


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
    ctime = time.strftime('%-I:%M %p')
    texpert.insert('insert', ctime, "a", ' ')


def date_com():
    cdate = time.strftime('%-m/%d/%Y')
    texpert.insert('insert', cdate, "a", ' ')


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
    \nMade in Python with tkinter\n\n""")
    bout.pack()
    cre = tk.Button(win, text="Credits", width=4, command=credits_com)
    cre.pack(side='left', padx=18, pady=4)
    clo = tk.Button(win, text="Close", width=4, command=win.destroy)
    clo.pack(side='right', padx=18, pady=4)
    win.transient(root)
    win.geometry('300x224+638+298')
    win.wait_window()


def credits_com():
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 0)
    win.title("Credits")
    cred = tk.Label(win, foreground="#404040",
                    text="""\n\n\nCreated by David Lawson
    \n\nme = Person()\nwhile (me.awake()):\nme.code()\n""")
    cred.pack()
    cls = tk.Button(win, text="Close", width=4, command=win.destroy)
    cls.pack(padx=8, pady=8)
    win.transient(root)
    win.geometry('300x224+638+298')
    win.wait_window()


#context menu (right-click)
def r_click(event):
    editmenu.tk_popup(event.x_root, event.y_root)
texpert.bind("<Button-3>", r_click)


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
is_notearea = tk.BooleanVar()
is_notearea.trace('w', lambda *args: note_area())
toolmenu.add_checkbutton(label="Note Area", variable=is_notearea)


#Help
helpmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=helpmenu)
helpmenu.add_command(label="About", command=about_com)


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
