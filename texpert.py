import os
import sys
import time
import datetime

try:
	import Tkinter as tk
	from ScrolledText import *
	import tkFileDialog
	import tkMessageBox
	import ttk
except:
	import tkinter as tk
	import tkinter.ttk as ttk
	import tkinter.filedialog as tkFileDialog
	import tkinter.messagebox as tkMessageBox
	from tkinter.scrolledtext import ScrolledText

try:
	import idlelib
	import idlelib.colorizer
	from idlelib.percolator import Percolator
	from idlelib import configdialog
except:
	popup = tk.Tk()
	popup.withdraw()
	tkMessageBox.showerror("Error", "Could not import `idlelib`, colour formatting disabled")
	popup.destroy()

class texpert_win:
	def __init__(self, master):
		self.master = master

		self.menu = tk.Menu(self.master, bd=1, relief='flat')
		self.master.config(menu=self.menu, bd=1)

		self.texpert = CustomText(self.master, bg="white", undo=True, font=("Arial", 11))
		self.texpert.grid(row=0, column=0, sticky='nsew')
		self.texpert.focus_set()
		#self.texpert.bind('<Key>', self.colour_in)

		# toolBar
		self.toolbar = tk.Frame(self.master, bd=2, relief='groove')
		self.open_butt = tk.Button(self.toolbar, text="Open", width=4, command=self.open_com)
		self.open_butt.pack(side=tk.LEFT, padx=4, pady=2)

		self.save_butt = tk.Button(self.toolbar, text="Save", width=4, command=self.saveas_com)
		self.save_butt.pack(side=tk.RIGHT, padx=4, pady=2)
		self.toolbar.grid(row=1, column=0, sticky='ew')

		#file menu
		self.filemenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="File ", menu=self.filemenu)
		self.filemenu.add_command(label="New", command=self.new_com)
		self.filemenu.add_command(label="Open", command=self.open_com)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Save", command=self.saveas_com)
		self.filemenu.add_command(label="Save As", command=self.saveas_com)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Close", command=self.close_com)
		self.filemenu.add_command(label="Exit", command=self.exit_com, underline=1)

		#edit menu
		self.editmenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Edit ", menu=self.editmenu)
		self.editmenu.add_command(label="Undo", command=self.undo_com)
		self.editmenu.add_command(label="Redo", command=self.redo_com)
		self.editmenu.add_separator()
		self.editmenu.add_command(label="Cut", command=self.cut_com)
		self.editmenu.add_command(label="Copy", command=self.copy_com)
		self.editmenu.add_command(label="Paste", command=self.paste_com)
		self.editmenu.add_separator()
		self.editmenu.add_command(label="Select All", command=self.select_all)

		#view menu
		self.viewmenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="View ", menu=self.viewmenu)
		self.toolbar_visible = tk.BooleanVar()
		self.toolbar_visible.set(True)
		self.viewmenu.add_checkbutton(label="Show Toolbar", variable=self.toolbar_visible,command=self.show_hide_toolbar, state='normal')
		self.inherit_idle_sett = tk.BooleanVar()
		if 'idlelib' in sys.modules:
			self.viewmenu.add_checkbutton(label="Inherit IDLE settings", variable=self.inherit_idle_sett, command=self.refresh_sett, state='normal')
			self.master.instance_dict = {}
			self.viewmenu.add_command(label="Configure IDLE", command=lambda: configdialog.ConfigDialog(self.master, 'IDLE Settings'), state='normal')
		else:
			self.viewmenu.add_command(label="Inherit IDLE settings", command=self.show_toolbar, state='disabled')
		self.viewmenu.add_separator()

		#sub-menu for: [view > mode]
		self.submenu = tk.Menu(self.menu, tearoff=0)
		self.viewmenu.add_cascade(label="Mode ", menu=self.submenu)
		self.submenu.add_command(label=" Dark", command=self.dark_mode, activebackground="#181818", activeforeground="#F5F5F5")
		self.submenu.add_command(label=" Light", command=self.light_mode, activebackground="#F5F5F5", activeforeground="#181818")
		self.submenu.add_command(label=" Legal Pad", command=self.legal_mode, activebackground="#FFFFCC", activeforeground="#181818")
		self.submenu.add_command(label=" Night Vision", command=self.green_mode, activebackground="#181818", activeforeground="#00FF33")
		self.submenu.add_command(label=" Desert View", command=self.desert_mode, activebackground="#E9DDB3", activeforeground="#40210D")
		self.submenu.add_command(label=" Chocolate Mint", command=self.mint_mode, activebackground="#BDFCC9", activeforeground="#40210D")

		self.viewmenu.add_separator()
		self.viewmenu.add_command(label="Hide in Tray", command=self.tray_com)
		self.viewmenu.add_command(label="Default", command=self.default_com)
		self.viewmenu.add_command(label="Fullscreen", command=self.full_com)

		#tool menu
		self.toolmenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Tools ", menu=self.toolmenu)
		self.toolmenu.add_command(label="Insert Time", command=self.time_com)
		self.toolmenu.add_command(label="Insert Date", command=self.date_com)
		self.toolmenu.add_command(label="Note Area", command=self.note_area)

		#help menu
		self.helpmenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Help ", menu=self.helpmenu)
		self.helpmenu.add_command(label="About", command=self.about_com)
		self.helpmenu.add_command(label="Troubleshooting", command=self.trouble_com)


		self.status = tk.Label(text=" Mode: Light", anchor=tk.W, bd=1, relief='sunken', fg='#000000', font=("Arial", 10))
		self.status.grid(row=2, column=0, sticky='ew')

		self.texpert.bind("<Control-Key-a>", self.select_all)
		self.texpert.bind("<Control-Key-A>", self.select_all)
		self.texpert.bind("<Button-3>", self.r_click)

		self.current_file = None
		self.file_type = None

		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_columnconfigure(0, weight=1)


	def r_click(self, event):
		self.editmenu.tk_popup(event.x_root, event.y_root)

	# Menu Functions
	# file menu
	def new_com(self):
		self.master.title("Untitled ")
		file = None
		self.texpert.delete(1.0, 'end-1c')

	def open_com(self, action='dialog'):
		if action == 'dialog':
			file = tkFileDialog.askopenfile(parent=self.master, mode='rb', title='Select File')
		elif action == 'current':
			file = self.current_file
		if file is not None:
			self.current_file = file.name
			contents = file.read()
			self.texpert.delete(1.0, 'end-1c')
			self.texpert.insert('1.0', contents)
			file.close()
			if str(self.current_file)[-3:] == '.py':
				self.file_type = 'Python'
				self.refresh_sett()


	def save_com(self):
		print ("Silent Save")

	def saveas_com(self):
		file = tkFileDialog.asksaveasfile(mode='w')
		if file is not None:
			data = self.texpert.get('1.0', 'end-1c')
			file.write(data)
			file.close()

	def close_com(self):
		self.master.title('')
		file = None
		self.texpert.delete(1.0, 'end-1c')

	def exit_com(self):
		if tkMessageBox.askokcancel("Exit", "Do you really want to exit? "):
			self.master.destroy()

	# edit menu
	def undo_com(self):
		self.texpert.edit_undo()

	def redo_com(self):
		self.texpert.edit_redo()

	def cut_com(self):
		self.texpert.event_generate("<<Cut>>")

	def copy_com(self):
		self.texpert.event_generate("<<Copy>>")

	def paste_com(self):
		self.texpert.event_generate("<<Paste>>")

	def select_all(self, event=None):
		self.texpert.tag_add(tk.SEL, '1.0', 'end-1c')
		self.texpert.mark_set(tk.INSERT, '1.0')
		self.texpert.see(tk.INSERT)
		return 'break'

	def show_hide_toolbar(self):
		if not self.toolbar_visible.get():
			self.hide_toolbar()
		else:
			self.show_toolbar()

	# view menu
	def hide_toolbar(self):
		self.toolbar.grid_forget()

	def show_toolbar(self):
		self.toolbar.grid(row=1, column=0, sticky='ew')

	#sub-menu for: [view > mode]
	def dark_mode(self):

		self.status["text"] = " Mode: Dark"
		self.texpert.config(background='#181818', fg='#F5F5F5', insertbackground='#F5F5F5')

	def light_mode(self):

		self.status["text"] = " Mode: Light"
		self.texpert.config(background='#F5F5F5', fg='#181818', insertbackground='#181818')

	def legal_mode(self):

		self.status["text"] = " Mode: Legal Pad"
		self.texpert.config(background='#FFFFCC', fg='#181818', insertbackground='#181818')

	def green_mode(self):

		self.status["text"] = " Mode: Night Vision"
		self.texpert.config(background='#181818', fg='#00FF33', insertbackground='#00FF33')

	def desert_mode(self):

		self.status["text"] = " Mode: Desert View"
		self.texpert.config(background='#E9DDB3', fg='#40210D', insertbackground='#40210D')


	def mint_mode(self):
		self.status["text"] = " Mode: Chocolate Mint"
		self.texpert.config(background='#BDFCC9', fg='#40210D', insertbackground='#40210D')

	def tray_com(self):
		self.master.iconify()

	def default_com(self):
		self.master.attributes('-zoomed', False)
		self.master.geometry("700x440+440+195") #default window size+position

	def full_com(self):
		self.master.attributes('-zoomed', True)

	# tools menu
	def time_com(self):
		ctime = time.strftime('%I:%M %p')
		self.texpert.insert(tk.INSERT, ctime, "a")

	def date_com(self):
		full_date = time.localtime()
		day = str(full_date.tm_mday)
		month = str(full_date.tm_mon)
		year = str(full_date.tm_year)
		date = ""+month+'/'+day+'/'+year
		self.texpert.insert(tk.INSERT, date, "a")


	# note area
	def note_area(self):
		note = tk.LabelFrame(self.texpert, bd=0)
		btn_frame = tk.Frame(note)

		tx = tk.Text(note, height=22, width=18, relief='ridge')
		tx.insert('1.0', 'Notes here\nwill not be saved..')
		#tx.bind("<FocusIn>", lambda args: tx.delete('0.0', 'end'))
		tx.pack(side='top', fill=tk.BOTH, expand=True)

		a = tk.Button(note, text="Clear", width=4, command=lambda: tx.delete('1.0', tk.END))
		a.pack(side='left', anchor=tk.S, padx=2, pady=2)
		b = tk.Button(note, text="Close", width=4, command=note.destroy)
		b.pack(side='right', anchor=tk.S, padx=2, pady=2)

		note.pack(side='right', fill=tk.Y, padx=0, pady=0)
		btn_frame.pack(side='bottom', fill=tk.Y)


	# help menu
	def about_com(self):
		win = tk.Toplevel()
		win.title("About")
		tk.Label(win, foreground='black', text="\n\n\nTexpert\n\nA small text editor designed for Linux.\n\nMade in Python with Tkinter\n\n\n").pack()

		a = tk.Button(win, text="Credits", width=4, command=self.credits_com)
		a.pack(side=tk.LEFT, padx=8, pady=4)
		b = tk.Button(win, text="Close", width=4, command=win.destroy)
		b.pack(side=tk.RIGHT, padx=8, pady=4)

		win.transient(self.master)
		win.geometry('300x200')
		win.wait_window()

	def credits_com(self): #linked to: [about > credits]
		win = Toplevel()
		win.wm_attributes("-topmost", 0)
		win.title("Credits")
		tk.Label(win, foreground='#606060', text="\n\n\nCreated by David Lawson\n\n\nme = Person()\nwhile (me.awake()):\nme.code()\n\n").pack()

		a = tk.Button(win, text="License", width=4, command=self.license_info)
		a.pack(side=tk.LEFT, padx=8, pady=4)
		b = tk.Button(win, text="Close", width=4, command=win.destroy)
		b.pack(side=tk.RIGHT, padx=8, pady=4)

		win.transient(self.master)
		win.geometry('300x200')
		win.wait_window()

	def license_info(self):
		win = tk.Toplevel()
		win.wm_attributes("-topmost", 1)
		win.title("License")
		tk.Label(win, foreground='black', justify='left', text="""\n\nMIT License

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
	PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
	THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
	DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
	CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
	IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
	DEALINGS IN THE SOFTWARE.\n""").pack()

		tk.Button(win, text='Close', command=win.destroy).pack()
		win.transient(self.master)
		win.geometry('504x435')
		win.wait_window()


	def trouble_com(self):
		win = tk.Toplevel()
		win.title("Troubleshooting")
		warning_text = "\n\nThis program was designed for Linux and\nmay not work on other operating systems. \n\nTexpert text editor is a work in progress\nand will probably never be complete.\n\n\nKnown Issues:\n\n'Show toolbar' is temporarily disabled\nbecause the toolbar refuses to remember\nits original position. I may or may not\nmake an attempt to fix this someday.\n\nThe 'Save' and 'Save As' options both work\nas 'save as'. This might be fixed someday.\n\n"
		tk.Label(win, foreground='black', justify='left', text=warning_text).pack()
		tk.Button(win, text='Close', command=win.destroy).pack()
		win.transient(self.master)
		win.geometry('340x350')
		win.wait_window()


	def refresh_sett(self):
		text = self.texpert.get('1.0', tk.END)
		self.texpert.destroy()
		self.texpert.frame.destroy()
		del self.texpert
		self.texpert = CustomText(self.master, bg="white", undo=True, font=("Arial", 11))
		self.texpert.grid(row=0, column=0, sticky='nsew')
		self.texpert.insert(tk.END, text)
		self.texpert.focus_set()

		self.texpert.colour_py(self.inherit_idle_sett.get())

class CustomText(tk.Text):
	'''
	The highlight_pattern method is a simplified python
	version of the tcl code at http://wiki.tcl.tk/3246
	'''
	def __init__(self, master=None, **kw):
		self.frame = tk.Frame(master)
		self.frame.grid_rowconfigure(0, weight=1)
		self.frame.grid_columnconfigure(0, weight=1)

		if 'wrap' not in kw:
			kw['wrap'] = 'none'


		self.vbar = tk.Scrollbar(self.frame, command=self.yview)
		kw.update({'yscrollcommand': self._scroll(self.vbar)})

		self.hbar = tk.Scrollbar(self.frame, command=self.xview, orient=tk.HORIZONTAL)
		kw.update({'xscrollcommand': self._scroll(self.hbar)})

		tk.Text.__init__(self, self.frame, **kw)
		self.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
		self.vbar.grid(row=0, column=1, sticky='nsew')
		self.hbar.grid(row=1, column=0, sticky='nsew')
		self['xscrollcommand'] = self._scroll(self.hbar)
		self['yscrollcommand'] = self._scroll(self.vbar)


		self._orig = self._w + "_original"
		self.tk.call("rename", self._w, self._orig)
		self.tk.createcommand(self._w, self._rework)


		# Copy geometry methods of self.frame without overriding Text
		# methods -- hack!
		text_meths = vars(tk.Text).keys()
		methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
		methods = methods.difference(text_meths)

		for m in methods:
			if m[0] != '_' and m != 'config' and m != 'configure':
				setattr(self, m, getattr(self.frame, m))

	def __str__(self):
		return str(self.frame)

	def _rework(self, command,*args):
		'''Bind <<TextModified>> to a custom command'''
		cmd = (self._orig, command) + args
		result = self.tk.call(cmd)

		if command in ("insert", "delete", "replace"):
			self.event_generate("<<TextModified>>")

		return result

	@staticmethod
	def _scroll(sbar):
		'''Hide and show scrollbar as needed'''
		def wrapped(first, last):
			first, last = float(first), float(last)
			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def colour_py(self, inherit_config=True):
		if 'idlelib' in sys.modules:
			col = idlelib.colorizer
			if inherit_config:
				col.color_config(self)
			p = Percolator(self)
			d = col.ColorDelegator()
			p.insertfilter(d)



def main():
	root = tk.Tk(className = "Texpert")
	root.geometry("700x440")
	root.title("Texpert")
	root.option_add("*Font", "TkDefaultFont 9")
	texpert_gui = texpert_win(root)
	root.mainloop()

if __name__ == '__main__':
	main()
