import sys
from cmd import Cmd

from addressbook import Contact, AddressBook
import utils
import validate
import math
import add
from cli import CONTACT_FIELDS, FIELD_VALIDATORS, REQUIRED_FIELDS
import tkFileDialog 

from Tkinter import *
import tkMessageBox 
root=Tk()


SCROLLAREA_WIDTH=700

ROW_PAD=20
COLUMN_PAD=20

BOX_HEIGHT= 270
BOX_WIDTH = 300

BOX_COLOR = '#ebebeb'
TEXT_WIDTH = BOX_WIDTH-40

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


class GUI(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		
		self.searchState = None
		
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=0)
		self.grid_columnconfigure(1, weight=0)
		self.grid_columnconfigure(2, weight=0)
		self.grid_columnconfigure(3, weight=7)
		self.grid_columnconfigure(4, weight=2)
		
		img1 = PhotoImage(file="add.gif")
		addBtn = Button(self, image= img1, command = self.clickAbout)
		addBtn.image = img1
		addBtn.grid(sticky = N+W, row = 0, column = 0, ipadx=0, padx=3, ipady=0, pady=3)
		

		img2 = PhotoImage(file="edit.gif")
		editBtn = Button(self, image=img2, command = self.clickEdit)
		editBtn.image = img2
		editBtn.grid(sticky = N+W, row = 0, column = 1, ipadx=0, padx=3, ipady=0, pady=3)

		img3 = PhotoImage(file="delete.gif")
		delBtn = Button(self, image=img3, command = self.clickDelete)
		delBtn.image = img3
		delBtn.grid(sticky = N+W, row = 0, column = 2, ipadx=0, padx=3, ipady=0, pady=3)
		
		self.grid(row = 0, column = 3, padx=20)
		
		self.searchBox = Entry(self, relief=SUNKEN, border=2, width=20)
		self.searchBox.grid(sticky = N+E, row = 0, column = 4, padx=2, pady=5)

		searchBtn = Button(self, text="Search", command = self.clickSearch)
		searchBtn.grid(sticky = N+E, row = 0, column = 5, padx=0, pady=5)
		
		searchBtn = Button(self, text="View Full Book", command = self.update)
		searchBtn.grid(sticky = N+E, row = 0, column = 6, padx=0, pady=5)
		
		self.tempvars = []
		self.tempID = -1
		self.addressbook = AddressBook()
		
		self.tempFile = None


		'''for i in range (0, 5):
			new_contact = Contact()
			setattr(new_contact, 'lname', "Yablok" + str(i))
			self.addressbook.add(new_contact)'''
		
		self.canvas=Canvas(self, relief=SUNKEN, border=2, bg='#c6c6c6')
		self.vbar=Scrollbar(self, command=self.canvas.yview)
		#self.vbar.grid(sticky=SW, side =RIGHT, fill=Y)
		self.vbar.config(command=self.canvas.yview)
		self.vbar.grid(sticky=NS, columnspan=8, row = 1, column = 8)

	
		self.canvas.config(width=980,height=700)
		self.canvas.config(yscrollcommand=self.vbar.set)
		#self.canvas.sticky(anchor=SE, side=LEFT,expand=True,fill=BOTH)
		self.canvas.grid(sticky=N+E+S+W, columnspan=7, row = 1, column = 0)

		self.fill_book()

		self.initUI()
    
	def initUI(self):
		self.parent.title("Blue Book")
		self.pack(fill=BOTH, expand=1)

	def get_current_box(self):
		id, = self.canvas.find_withtag('current')
		tags = self.canvas.gettags('current')
		if 'text' in tags: # the current item is the text in the box
			id = self.canvas.find_withtag(self.canvas.itemcget(id,'text'))
		return id;
		
	def get_selected_box(self):
		id, = self.canvas.find_withtag('select')
		tags = self.canvas.gettags('select')
		if 'text' in tags: # the current item is the text in the box
			id = self.canvas.find_withtag(self.canvas.itemcget(id,'text'))
		return id;
        
	def enter_callback(self, event):
		id = self.get_current_box()


	def leave_callback(self, event):
		id = self.get_current_box()

                 
	def select_callback(self, event):
		id = self.get_current_box()
		tags=self.canvas.gettags(id)
		for t in tags:
			if (t == "select"):
				self.canvas.dtag(id, 'select')
				self.canvas.itemconfigure(id, width=0, fill=BOX_COLOR)
				return

		for en in self.canvas.find_withtag("select"):
			if (en != id):
				self.canvas.dtag(en, 'select')
				self.canvas.itemconfigure(en, width=0, fill=BOX_COLOR)
		self.canvas.addtag('select', 'withtag', id)
		self.canvas.itemconfigure(id, width=2, outline="#65c3f3", fill="#FFFFFF")
            
	def fill_book(self):
		SCROLLAREA_HEIGHT = (BOX_HEIGHT + ROW_PAD)*int(math.ceil(self.addressbook.total/3.0)) + ROW_PAD
		self.canvas.config(scrollregion=(0,0,SCROLLAREA_WIDTH, SCROLLAREA_HEIGHT))
		
		if self.addressbook.total == 0:
			self.canvas.create_text(980/2, 700/2, anchor='c', tags='text', text="The addressbook is currently empty.", )
	
		else:
			idn = 0
			r = 0
			y = COLUMN_PAD
			for c in range(0, self.addressbook.total):
				if (idn%3 == 0 and idn != 0):
					r += 1
					y = COLUMN_PAD+r*(BOX_HEIGHT+COLUMN_PAD)
					x = ROW_PAD
				else :
					x = ROW_PAD+((c%3)*(BOX_WIDTH+ROW_PAD))
					y = COLUMN_PAD+r*(BOX_HEIGHT+COLUMN_PAD)
				if (idn < self.addressbook.total):
					id = self.canvas.create_rectangle(x, y, x+BOX_WIDTH, y+BOX_HEIGHT, fill=BOX_COLOR, width=0, tags=('box', idn )) 
					con = ""
					for field in CONTACT_FIELDS:
						if (getattr(self.addressbook.contacts[idn], field[0], '') != ""):
							con += field[1] + ": " + str(getattr(self.addressbook.contacts[idn], field[0], '') + "\n")
					self.canvas.create_text(x+20, y+20, anchor='nw', text=con, tags='text', width=TEXT_WIDTH)
				idn+= 1
        	self.canvas.tag_bind('all', '<Any-Enter>', self.enter_callback )
        	self.canvas.tag_bind('all', '<Any-Leave>', self.leave_callback )
        	self.canvas.tag_bind('all', '<1>', self.select_callback )
        	

	def sub_fill_book(self, subset):
		SCROLLAREA_HEIGHT = (BOX_HEIGHT + ROW_PAD)*int(math.ceil(self.addressbook.total/3.0)) + ROW_PAD
		self.canvas.config(scrollregion=(0,0,SCROLLAREA_WIDTH, SCROLLAREA_HEIGHT))
		
		if len(subset) == 0:
			self.canvas.create_text(980/2, 700/2, anchor='c', tags='text', text="There were no results found for this search.")
	
		else:
			idn = 0
			r = 0
			y = COLUMN_PAD
			for c in range(0, len(subset)):
				if (idn%3 == 0 and idn != 0):
					r += 1
					y = COLUMN_PAD+r*(BOX_HEIGHT+COLUMN_PAD)
					x = ROW_PAD
				else :
					x = ROW_PAD+((c%3)*(BOX_WIDTH+ROW_PAD))
					y = COLUMN_PAD+r*(BOX_HEIGHT+COLUMN_PAD)
				if (idn < self.addressbook.total):
					id = self.canvas.create_rectangle(x, y, x+BOX_WIDTH, y+BOX_HEIGHT, fill=BOX_COLOR, width=0, tags=('box', idn )) 
					con = ""
					for field in CONTACT_FIELDS:
						if (getattr(subset[idn][1], field[0], '') != ""):
							con += field[1] + ": " + str(getattr(subset[idn][1], field[0], '') + "\n")
					self.canvas.create_text(x+20, y+20, anchor='nw', text=con, tags='text', width=TEXT_WIDTH)
				idn+= 1
        	self.canvas.tag_bind('all', '<Any-Enter>', self.enter_callback )
        	self.canvas.tag_bind('all', '<Any-Leave>', self.leave_callback )
        	self.canvas.tag_bind('all', '<1>', self.select_callback )

	def update(self):
		self.searchState = None
		self.searchBox.delete(0, 10000)
		self.canvas.delete("all")
		self.fill_book()
		
	def sort(self):
		if (self.searchState is None):
			if (self.addressbook.total == 0):
				return
			self.addressbook.sort()
		else:
			if (len(self.searchState) == 0):
				return
			self.addressbook.sort(self.searchState)
		self.update()

	def clickSearch(self):
		results = []
		val = self.searchBox.get()
		for field in (CONTACT_FIELDS):
			results += self.addressbook.search(field[0], val)
		self.canvas.delete("all")
		self.sub_fill_book(results)
		self.searchState=results

	def clickAbout(self):
		self.tempvars = []
		toplevel = Toplevel()
		toplevel.title("Add an Entry")
		count = 1
		tex = Label(toplevel, text="Please enter your new contact information in the inputs below.")
		tex.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=10, pady=10)
		for label in (CONTACT_FIELDS):
			va = StringVar()
			l = Label(toplevel, text=label[1])
			l.grid(row=count,column=0, columnspan=1, sticky=W, padx=10, pady=3)
			e = Entry(toplevel, relief=SUNKEN, border=2, width=40, textvariable=va)
			e.grid(row=count,column=1, columnspan=3, sticky=W, padx=10, pady=3)
			self.tempvars.append(e)
			count += 1
		ok = Button(toplevel, text="Submit", command=combine_funcs(self.addEntry, toplevel.destroy))
		can = Button(toplevel, text="Cancel", command=toplevel.destroy)
		can.grid(row=count,column=2, sticky=W, padx=0, pady=10)
		ok.grid(row=count,column=1, sticky=W, padx=0, pady=10)
		

	def addEntry(self):
		new_contact = Contact()
		count = 0
		for field in CONTACT_FIELDS:
			data = self.tempvars[count].get()
			setattr(new_contact, field[0], data)
			"""if (not valid):
				tkMessageBox.showinfo("Input error", "Something was invalid")"""
			count += 1
		self.addressbook.add(new_contact)
		self.canvas.delete("all")
		self.fill_book()
		
		

	def clickEdit(self):
		self.tempvars = []
		self.tempID = -1
		if (len(self.canvas.find_withtag('select')) == 0 or self.addressbook.total == 0):
			tkMessageBox.showinfo("Error: No Selection", "Please select an address to edit by clicking on its surrounding box. Selected addresses will have a blue outline.")
			return

		toplevel = Toplevel()
		toplevel.title("Edit an Entry")
		id = self.get_selected_box()
		tags=self.canvas.gettags(id)
		for t in tags:
			if t not in ('current','box', 'select'):
				box_name=t
		try:
			i = int(box_name)
		except ValueError:
			tkMessageBox.showinfo("Input error", "Something was invalid")
			return
		self.tempID = i;
		count = 1
		tex = Label(toplevel, text="Please enter your new contact information in the inputs below.")
		tex.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=10, pady=10)
		for label in (CONTACT_FIELDS):
			va = StringVar()
			l = Label(toplevel, text=label[1])
			l.grid(row=count,column=0, columnspan=1, sticky=W, padx=10, pady=3)
			if (self.searchState is None):
				s = str(getattr(self.addressbook.contacts[i], label[0], ''))
			else:
				s = str(getattr(self.searchState[i][1], label[0], ''))
			va.set(s)
			e = Entry(toplevel, relief=SUNKEN, border=2, width=40, text=s, textvariable=va)
			e.grid(row=count,column=1, columnspan=3, sticky=W, padx=10, pady=3)
			self.tempvars.append(e)
			count += 1
		ok = Button(toplevel, text="Submit", command=combine_funcs(self.editEntry, toplevel.destroy))
		can = Button(toplevel, text="Cancel", command=toplevel.destroy)
		can.grid(row=count,column=2, sticky=W, padx=0, pady=10)
		ok.grid(row=count,column=1, sticky=W, padx=0, pady=10)
		

	def editEntry(self):
		if (self.tempID >= 0):
			en = self.addressbook.contacts[self.tempID]
			count = 0
			for field in CONTACT_FIELDS:
				data = self.tempvars[count].get()
				if (data != ""):
					setattr(en, field[0], data)
				"""if (not valid):
					tkMessageBox.showinfo("Input error", "Something was invalid")"""
				count += 1
			self.canvas.delete("all")
			self.fill_book()
			
		else: 
			tkMessageBox.showinfo("Input error", "Something was invalid")
			return
			

	def clickDelete(self):
		self.tempvars = []
		self.tempID = -1
		if (len(self.canvas.find_withtag('select')) == 0 or self.addressbook.total == 0):
			tkMessageBox.showinfo("Error: No Selection", "Please select an address to edit by clicking on its surrounding box. Selected addresses will have a blue outline.")
			return

		id = self.get_selected_box()
		tags=self.canvas.gettags(id)
		for t in tags:
			if t not in ('current','box', 'select'):
				box_name=t
		try:
			i = int(box_name)
		except ValueError:
			tkMessageBox.showinfo("Input error", "Something was invalid")
			return
		self.tempID = i;


		con = ""
		for field in CONTACT_FIELDS:
			if (self.searchState is None):
				con += field[1] + ": " + getattr(self.addressbook.contacts[i], field[0], '') + "\n"
			else:
				con += field[1] + ": " + str(getattr(self.searchState[i][1], field[0], '')) + "\n"
		
		if tkMessageBox.askyesno("Delete an Entry", "Are you sure you want to delete this entry?\n" + con):
			if (self.searchState is None):
				self.addressbook.delete(i)
			else:
				self.addressbook.delete(self.searchState[i][0])
			self.canvas.delete("all")
			self.fill_book()

	def new(self):
		self.tempFile = None
		if tkMessageBox.askyesno("New Address Book", "Are you sure you want to create a new file? \n (Remember to save your Address Book first)"):
			self.addressbook.contacts = []
			self.addressbook.total = 0
			self.canvas.delete("all")
			self.fill_book()
			
	def open(self):
		if tkMessageBox.askyesno("New Address Book", "Are you sure you want to open a new file? \n (Remember to save your Address Book first)"):
			self.addressbook.contacts = []
			self.addressbook.total = 0
			self.canvas.delete("all")
			self.imp()
			self.fill_book()

	def close(self):
		if tkMessageBox.askyesno("New Address Book", "Are you sure you want to close this address book? \n (Remember to save your Address Book first)"):
			self.addressbook.contacts = []
			self.addressbook.total = 0
			self.canvas.delete("all")
			self.imp()
			self.fill_book()
		
	def imp(self):
		self.tempFile = None
		ftypes = [('TSV files', '*.tsv'), ('All files', '*')]
		dlg = tkFileDialog.Open(self, filetypes = ftypes)
		fl = dlg.show()

		if fl != '':
			self.addressbook.import_contacts(fl)
			self.canvas.delete("all")
			self.fill_book()
			
	def export(self):
		f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".tsv")
		if f is None:
			return
		self.tempFile = f.name
		self.addressbook.export_contacts(f.name)

	def save(self):
		if (self.tempFile is None):
			self.export()
		else:
			self.addressbook.export_contacts(self.tempFile)

def main():
	root.geometry("250x150+300+300")
	app = GUI(root)

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=app.new)
	filemenu.add_command(label="Open", command=app.open)
	filemenu.add_command(label="Close", command=app.new)
	filemenu.add_command(label="Save", command=app.save)
	filemenu.add_command(label="Save As...", command=app.export)
	filemenu.add_separator()
	filemenu.add_command(label="Import", command=app.imp)
	filemenu.add_command(label="Export", command=app.export)
	filemenu.add_separator()
	filemenu.add_command(label="Quit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	
	filemenu2 = Menu(menubar, tearoff=1)
	filemenu2.add_command(label="Add", command=app.clickAbout)
	filemenu2.add_command(label="Edit", command=app.clickEdit)
	filemenu2.add_command(label="Delete", command=app.clickDelete)
	submenu = Menu(filemenu2)
	submenu.add_command(label="Last Name", command=app.sort)
	submenu.add_command(label="ZIP Code")
	
	menubar.add_cascade(label="Edit", menu=filemenu2)
	filemenu2.add_cascade(label='Sort By...', menu=submenu, underline=0)	
	
	root.config(menu=menubar)    
	
	root.minsize(300,300)
	root.geometry("1000x780")
	root.mainloop()  


if __name__ == '__main__':
    main()  
