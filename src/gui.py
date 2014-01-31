"""
	Graphical-User Interface module.


	For simple Address Book applet - Project 1 -
	CIS 422, W'14, University of Oregon

	:author: Sarah Yablok <sarahy@cs.uoregon.edu>
"""

import sys
from cmd import Cmd

from addressbook import Contact, AddressBook
import utils
import validate
import math
from cli import CONTACT_FIELDS, FIELD_VALIDATORS, REQUIRED_FIELDS
import tkFileDialog 

from Tkinter import *
import tkMessageBox 
root=Tk()


SCROLLAREA_WIDTH = 700
ROW_PAD = 20
COLUMN_PAD = 20
BOX_HEIGHT = 240
BOX_WIDTH = 300
BOX_COLOR = '#ebebeb'
BOX_HIGHLIGHT = '#ffffff'
TEXT_WIDTH = BOX_WIDTH-40


def combine_funcs(*funcs):
	"""Simple function which takes two function commands, and combines their
		actions, one after another. (Used for closing toplevel window after adding
		or editing a contact."""
	def combined_func(*args, **kwargs):
		for f in funcs:
			f(*args, **kwargs)
	return combined_func


class GUI(Frame):
	"""Main class which represents our parent window for the GUI."""
	
	def __init__(self, parent):
		"""Initiates the window, with the appropriate grid layout, buttons,
			Canvas and scroll bar. All class-wide variables defined here."""
		Frame.__init__(self, parent, background="#ffffff")
		self.parent = parent
		
		#Temporary Variables - remember to reset!
		self.searchState = None #Currently displaying search results?
		self.tempvars = []	#Temporary values for add and editing fields
		self.tempID = -1	#TemporaryID number for contact
		self.tempFile = None	#Temporary File for import/export
		self.mL = 0		#Mailing label flag
		
		# Some formatting for the grid layout
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=2)
		self.grid_columnconfigure(1, weight=0)
		self.grid_columnconfigure(2, weight=0)
		self.grid_columnconfigure(3, weight=0)
		self.grid_columnconfigure(4, weight=7)

		#Logo Column
		logo = PhotoImage(file="logo.gif")
		imgCan = Label(self, image=logo)
		imgCan.image = logo
		imgCan.grid(sticky = N+W, row = 0, column = 0, padx=0)	
		
		# Add Button
		img1 = PhotoImage(file="add.gif")
		addBtn = Button(self, image= img1, command = self.clickAdd)
		addBtn.image = img1
		addBtn.grid(sticky = N+W, row = 0, column = 1, ipadx=5, padx=3, ipady=5, pady=8)
		
		# Edit Button
		img2 = PhotoImage(file="edit.gif")
		editBtn = Button(self, image=img2, command = self.clickEdit)
		editBtn.image = img2
		editBtn.grid(sticky = N+W, row = 0, column = 2, ipadx=5, padx=3, ipady=5, pady=8)

		#Delete Button
		img3 = PhotoImage(file="delete.gif")
		delBtn = Button(self, image=img3, command = self.clickDelete)
		delBtn.image = img3
		delBtn.grid(sticky = N+W, row = 0, column = 3, ipadx=5, padx=3, ipady=5, pady=8)
		
		#Search Box Input
		self.searchBox = Entry(self, relief=SUNKEN, border=2, width=20)
		self.searchBox.grid(sticky = N+E, row = 0, column = 4, padx=2, pady=20)

		#Search Button
		searchBtn = Button(self, text="Search", command = self.clickSearch)
		searchBtn.grid(sticky = N+E, row = 0, column = 5, padx=0, pady=20)
		
		#Return to view the full book Button
		search2Btn = Button(self, text="View Full Book", command = self.update)
		search2Btn.grid(sticky = N+E, row = 0, column = 6, padx=0, pady=20)
		
		#Main addressbook!
		self.addressbook = AddressBook()

		#Used for initial testing
		"""for i in range (0, 5):
			new_contact = Contact()
			setattr(new_contact, 'lname', "Yablok" + str(i))
			self.addressbook.add(new_contact)"""
		
		#Canvas and scrollbar configuration
		self.canvas=Canvas(self, relief=SUNKEN, border=2, bg='#c6c6c6')
		self.vbar=Scrollbar(self, command=self.canvas.yview)
		self.vbar.config(command=self.canvas.yview)
		self.vbar.grid(sticky=NS, columnspan=8, row = 1, column = 8)
		self.canvas.config(width=980,height=700)
		self.canvas.config(yscrollcommand=self.vbar.set)
		self.canvas.grid(sticky=N+E+S+W, columnspan=7, row = 1, column = 0)

		self.fill_book(self.addressbook.contacts)
		self.initUI()


	def initUI(self):
		"""Setup the window and display it.""" 
		self.parent.title("Blue Book")
		self.pack(fill=BOTH, expand=1)


	def get_tagged_box(self, tag):
		"""Search through Canvas objects by tags, return the rectangle with the given tag."""
		id, = self.canvas.find_withtag(tag)
		tags = self.canvas.gettags(tag)
		if 'text' in tags: #if the current item is text
			id = self.canvas.find_withtag(self.canvas.itemcget(id,'text'))
		return id;
 

	def boxClicked(self, event):
		"""Give the rectangle the 'select' tag when clicked, and the highlight properties
			(outline and white background."""
		id = self.get_tagged_box('current')
		tags = self.canvas.gettags(id)
		for t in tags:
			if (t == "select"): #The box is already selected, clicking should deselect
				self.canvas.dtag(id, 'select')
				self.canvas.itemconfigure(id, width=0, fill=BOX_COLOR)
				return
		for en in self.canvas.find_withtag("select"):
			if (en != id): #Cycle through and make sure only one is selected at a time.
				self.canvas.dtag(en, 'select')
				self.canvas.itemconfigure(en, width=0, fill=BOX_COLOR)
		#Select the current box.
		self.canvas.addtag('select', 'withtag', id)
		self.canvas.itemconfigure(id, width=2, outline="#58a4cd", fill=BOX_HIGHLIGHT)


	def hover(self, event):
		"""Binding for when the user hovers over a rectangle. Changes the cursor."""
		id = self.get_tagged_box('current')
		self.config(cursor="pointinghand")


	def no_hover(self,event):
		"""Binding for when the user stops hovering over a rectangle. Changes the cursor."""
		id = self.get_tagged_box('current')
		self.config(cursor="")


	def fill_book(self, subset):
		"""Fill the Canvas with the info from adresses from the subset provided.
			for each entry add a rectangle to the canvas, and the associated address text within
			the rectangle. Bind these boxes to the boxClicked() function."""
		SCROLLAREA_HEIGHT = (BOX_HEIGHT + ROW_PAD)*int(math.ceil(len(subset)/3.0)) + ROW_PAD
		self.canvas.config(scrollregion=(0,0,SCROLLAREA_WIDTH, SCROLLAREA_HEIGHT))
		
		if len(subset) == 0 and self.searchState is None:
			self.canvas.create_text(980/2, 700/2, anchor='c', tags='text', text="The addressbook is currently empty.", )
		elif len(subset) == 0:
			self.canvas.create_text(980/2, 700/2, anchor='c', tags='text', text="No existing entries match your search.", )
		else:
			idn = 0 #ID Number
			r = 0 #row count
			y = COLUMN_PAD
			
			for c in range(0, len(subset)):
				if (idn%3 == 0 and idn != 0): #If in a new row
					#Update row count, x, and y.
					r += 1
					y = COLUMN_PAD+r*(BOX_HEIGHT+COLUMN_PAD)
					x = ROW_PAD
				else :
					x = ROW_PAD+((c%3)*(BOX_WIDTH+ROW_PAD))
					y = COLUMN_PAD+r*(BOX_HEIGHT+COLUMN_PAD)
				
				#If the index number exists in the addressbook
				if (idn < self.addressbook.total):
					#Create rectangle
					id = self.canvas.create_rectangle(x, y, x+BOX_WIDTH, y+BOX_HEIGHT, fill=BOX_COLOR, width=0, tags=('box', idn)) 
					con = ""
					#Generate Text
					for field in CONTACT_FIELDS:
						#Check for subset
						if (self.searchState is None): #default
							entry = self.addressbook.contacts[idn]
						else: #Data has been searched, get from tuple
							entry = subset[idn][1]
							
						if (getattr(entry, field[0], '') != ""):
							con += field[1] + ": " + str(getattr(entry, field[0], '') + "\n")
					#Check for Mailing Label Display
					if (self.mL):
						self.canvas.create_text(x+20, y+20, anchor='nw', text=entry.print_mailing(), tags='text', width=TEXT_WIDTH)
					else:
						self.canvas.create_text(x+20, y+20, anchor='nw', text=con, tags='text', width=TEXT_WIDTH)
				idn+= 1 #Increment ID Number
        	self.canvas.tag_bind('all', '<1>', self.boxClicked) #Check when box is clicked
        	self.canvas.tag_bind('all', '<Any-Enter>', self.hover) #Check when box is hovered over
        	self.canvas.tag_bind('all', '<Any-Leave>', self.no_hover) #Check when box is not hovered over


	def update(self):
		"""Update the canvas once a change has been made to the addressbook,
			to display changes in the addressbook we delete all entries and and
			re-fill the canvas via the fill_book() function."""
		self.searchState = None #reset searchState
		self.searchBox.delete(0, 10000)
		self.canvas.delete("all")
		self.fill_book(self.addressbook.contacts)


	def updateSearchState(self):
		"""Special update function which uses a subset of the full address
			book - the self.searchState which is the current search results."""
		self.canvas.delete("all")
		self.fill_book(self.searchState)
	

	def sort(self, att):
		"""Sort the addresses by last name. This search function only works
			on the full addressbook, not a subset, sort before searching."""
		#If we are not viewing search results, sort entire book
		if (self.addressbook.total == 0):
			return
		attrs = []
		attrs.append(att)
		attrs.extend(['lname', 'fname'])
		self.addressbook.sort(attributes=attrs)
		self.update()


	def clickSearch(self):
		"""General search for all of the fields and all of the contacts in the
			address book. It will look for exact matches in fields. For example search
			will accurately find '123 Easy St' but not just 'Easy St'. (Needs full search
			field."""
		results = []
		val = self.searchBox.get()
		if val == "":
			return
		for field in (CONTACT_FIELDS):
			results += self.addressbook.search(field[0], val)
		self.searchState = results
		self.updateSearchState()


	def clickAdd(self):
		"""Add an entry to the address book. Creates a new top level window with inputs, and refers
			to the addEntry function to add the new contact object."""
		self.tempvars = []
		self.searchState = None
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
		ok = Button(toplevel, text="Submit", command= lambda: self.addEntry(toplevel))
		can = Button(toplevel, text="Cancel", command=toplevel.destroy)
		can.grid(row=count,column=2, sticky=W, padx=0, pady=10)
		ok.grid(row=count,column=1, sticky=W, padx=0, pady=10)
		

	def addEntry(self, top):
		"""Get all of the fields entered by the user in the toplevel window
			Add the new contact object to the address book and update the canvas."""
		new_contact = Contact()
		count = 0
		go = 1
		for field in CONTACT_FIELDS:
			valid = FIELD_VALIDATORS[field[0]]
			if field[0] in REQUIRED_FIELDS:
				data = self.tempvars[count].get()
				if data == "":
					tkMessageBox.showinfo("Required Field Error", field[1] + " is a required field, please enter this info into the input box.")
					go = 0
					break
				if(go): setattr(new_contact, field[0], data)
			else:
				data = self.tempvars[count].get()
				if data != "" and not valid(data)[0]:
					tkMessageBox.showinfo("Input Error", valid(data)[1])
					go = 0
					break
				if(go): setattr(new_contact, field[0], data)
			count += 1
		if(go):
			self.addressbook.add(new_contact)
			self.update()
			top.destroy()		


	def clickEdit(self):
		"""Edit an existing entry in the address book. Creates a new top level window with
			inputs which automatically gets the existing fields from the contact selected by the user.
			It refers to the editEntry() function to make the edits in to the actual contact in the addressbook."""
		self.tempvars = [] #Temp values to get from the entry boxes
		self.tempID = -1 #Temp ID of the Contact being edited
		
		#ERROR: no contact selected by the user
		if (len(self.canvas.find_withtag('select')) == 0 or self.addressbook.total == 0):
			tkMessageBox.showinfo("Error: No Selection", "Please select an address to edit by clicking on its surrounding box. Selected addresses will have a blue outline.")
			return

		toplevel = Toplevel()
		toplevel.title("Edit an Entry")
		
		#Get the global ID of the contact based on
		#based on what is selected.
		id = self.get_tagged_box('select')
		tags=self.canvas.gettags(id)
		for t in tags:
			if t not in ('current','box', 'select'):
				box_name=t
		try:
			i = int(box_name)
		except ValueError:
			tkMessageBox.showinfo("Input error", "The ID of the contact is invalid, please delete and re-add this contact.")
			return
		self.tempID = i; #global ID
		
		#Layout configuration for the new toplevel window
		count = 1
		tex = Label(toplevel, text="Please edit the contact information in the inputs below.")
		tex.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=10, pady=10)
		for label in (CONTACT_FIELDS): #Get all of the fields
			va = StringVar()
			l = Label(toplevel, text=label[1])
			l.grid(row=count,column=0, columnspan=1, sticky=W, padx=10, pady=3)
			
			#Special case for if searchState is activated.
			if (self.searchState is None):
				s = str(getattr(self.addressbook.contacts[i], label[0], ''))
			else:
				s = str(getattr(self.searchState[i][1], label[0], ''))
			
			va.set(s)
			e = Entry(toplevel, relief=SUNKEN, border=2, width=40, text=s, textvariable=va)
			e.grid(row=count,column=1, columnspan=3, sticky=W, padx=10, pady=3)
			self.tempvars.append(e) # add the values so we can .get() them later
			count += 1
		ok = Button(toplevel, text="Submit", command=lambda: self.editEntry(toplevel))
		can = Button(toplevel, text="Cancel", command=toplevel.destroy)
		can.grid(row=count,column=2, sticky=W, padx=0, pady=10)
		ok.grid(row=count,column=1, sticky=W, padx=0, pady=10)	


	def editEntry(self, top):
		"""Edit the entry id in self.tempID. Update all of the fields, and update the
			Canvas to reflect these changes."""
		if (self.tempID >= 0):
		
			#special case for searchState subset 
			if (self.searchState is None):
				en = self.addressbook.contacts[self.tempID]
			else:
				en = self.searchState[self.tempID][1]
			
			count = 0
			go = 1
			for field in CONTACT_FIELDS:
				valid = FIELD_VALIDATORS[field[0]]
				if field[0] in REQUIRED_FIELDS:
					data = self.tempvars[count].get()
					if data == "":
						tkMessageBox.showinfo("Required Field Error", field[1] + " is a required field, please enter this info into the input box.")
						go = 0
						break
					if(go): setattr(en, field[0], data)
				else:
					data = self.tempvars[count].get()
					if data != "" and not valid(data)[0]:
						tkMessageBox.showinfo("Input Error", valid(data)[1])
						go = 0
						break
					if(go): setattr(en, field[0], data)
				count += 1
			if (go):
				if (self.searchState is None):
					self.update()
				else:
					self.updateSearchState()
				top.destroy()
			
		else: 
			tkMessageBox.showinfo("Input error", "The ID of the contact is invalid, please delete and re-add this contact")
			return
	

	def clickDelete(self):
		"""Delete a contact from the address book, prompt a confirmation box which
			reviews the contact information, and proceeds to delete the entry from
			the addressbook, and update the Canvas"""
		self.tempvars = [] #Temp values to get from the entry boxes
		self.tempID = -1 #Temp ID of the Contact being edited

		#ERROR: no contact selected by the user
		if (len(self.canvas.find_withtag('select')) == 0 or self.addressbook.total == 0):
			tkMessageBox.showinfo("Error: No Selection", "Please select an address to delete by clicking on its surrounding box. Selected addresses will have a blue outline.")
			return
		
		#Get the global id of the selected contacts
		#through the tags options
		id = self.get_tagged_box('select')
		tags = self.canvas.gettags(id)
		for t in tags:
			if t not in ('current','box', 'select'):
				box_name=t
		try:
			i = int(box_name)
		except ValueError:
			tkMessageBox.showinfo("Input error", "Something was invalid")
			return
		self.tempID = i; #Gloabl ID

		con = ""
		for field in CONTACT_FIELDS:
			#Special case for  searchState subset
			if (self.searchState is None):
				con += field[1] + ": " + getattr(self.addressbook.contacts[i], field[0], '') + "\n"
			else:
				con += field[1] + ": " + str(getattr(self.searchState[i][1], field[0], '')) + "\n"
		#Confirmation box
		if tkMessageBox.askyesno("Delete an Entry", "Are you sure you want to delete this entry?\n" + con):
			if (self.searchState is None):
				self.addressbook.delete(self.tempID)
			else:
				self.addressbook.delete(self.searchState[self.tempID][0])
				self.searchState.pop(self.tempID)
			
			#Update the Canvas
			if (self.searchState is None):
				self.update()
			else:
				self.updateSearchState()


	def mailLabels(self):
		"""View the contact information in a mailing label format.
			Update the canvas to display new format"""
		self.mL = 1
		if (self.searchState is None):
			self.update()
		else:
			self.updateSearchState()


	def noMailLabels(self):
		"""View the contact information in the regular format.
			Update the canvas to display new format"""
		self.mL = 0
		if (self.searchState is None):
			self.update()
		else:
			self.updateSearchState()


	def new(self):
		"""Create a new blank address book, ask to save before creating new book.
			Update the Canvas with the new book."""
		self.tempFile = None
		if tkMessageBox.askyesno("New Address Book", "Do you want to save your current file first?"):
			self.save()
		self.addressbook.contacts = []
		self.addressbook.total = 0
		self.update()
	

	def open(self):
		"""Open a new address book and prompt the user to save changes."""
		if self.addressbook.contacts != []: 
			if tkMessageBox.askyesno("Open Address Book", "Do you want to save your current file first?"):
				self.save()
		dlg = tkFileDialog.Open(self)
		fl = dlg.show()

		if fl != '':
			self.addressbook = utils.open_addressbook(fl)
			self.tempFile = fl
			self.update()


	def close(self):
		"""Close an address book and prompt the user to save changes. If no address book is open,
		quit the program"""
		if self.addressbook.contacts == []: 
			root.quit()
			return
		if tkMessageBox.askyesno("Close Address Book", "Do you want to save your current file first?"):
			self.save()
		self.tempFile = None
		self.addressbook.contacts = []
		self.addressbook.total = 0
		self.update()


	def imp(self):
		"""Import a new address from a .tsv file. Prompt the user to select a file,
			update the Canvas with the imported addressbook"""	
		ftypes = [('TSV files', '*.tsv'), ('All files', '*')]
		dlg = tkFileDialog.Open(self, filetypes = ftypes)
		fl = dlg.show()
		if fl != '':
			self.addressbook.import_contacts(fl)
			if tkMessageBox.askyesno("Import Addresses", 
				"Do you want to merge addresses with the same first and last name?"):
				self.addressbook.merge_addressbook()
			self.update()
	

	def export(self):
		"""Export the current address book to a .tsv file. Prompt the user to select a file,
		update the Canvas with the imported addressbook"""
		self.tempFile = None
		f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".tsv")
		if f is None:
			return
		self.tempFile = f.name
		self.addressbook.export_contacts(f.name)


	def save(self):
		"""Save an address book to the disk."""
		if (self.tempFile is None):
		    f = tkFileDialog.asksaveasfile()
		    if f != None and self.addressbook != None:
		    	utils.save_addressbook(self.addressbook, f.name)
		    	self.tempFile = f.name
		else:
			utils.save_addressbook(self.addressbook, self.tempFile)


	def save_as(self):
		"""Save an address book to the disk prompting for a file name."""
		f = tkFileDialog.asksaveasfile()
		if f != None and self.addressbook != None:
		    utils.save_addressbook(self.addressbook, f.name)


	def quit(self):
		"""Quit the program but make sure to save changes first."""
		self.close()
		root.quit()


def main():
	"""Create the GUI class with the root window. Configure the
		menu bars."""
	root.geometry("250x150+300+300")

	app = GUI(root)

	menubar = Menu(root)
	
	# Close button 
	root.protocol('WM_DELETE_WINDOW', app.quit)

	# File Menu
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=app.new)
	filemenu.add_command(label="Open", command=app.open)
	filemenu.add_command(label="Close", command=app.close)
	filemenu.add_command(label="Save", command=app.save)
	filemenu.add_command(label="Save As...", command=app.save_as)
	filemenu.add_separator()
	filemenu.add_command(label="Import", command=app.imp)
	filemenu.add_command(label="Export", command=app.export)
	filemenu.add_separator()
	filemenu.add_command(label="Quit", command=app.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	
	# Edit Menu
	filemenu2 = Menu(menubar, tearoff=1)
	filemenu2.add_command(label="Add", command=app.clickAdd)
	filemenu2.add_command(label="Edit", command=app.clickEdit)
	filemenu2.add_command(label="Delete", command=app.clickDelete)
	submenu = Menu(filemenu2)
	submenu.add_command(label="First Name", command= lambda: app.sort('fname'))
	submenu.add_command(label="Last Name", command= lambda: app.sort('lname'))
	submenu.add_command(label="City", command= lambda: app.sort('city'))
	submenu.add_command(label="State", command= lambda: app.sort('state'))
	submenu.add_command(label="ZIP Code", command= lambda: app.sort('zipcode'))

	submenu2 = Menu(filemenu2)
	submenu2.add_command(label="Mailing Labels", command=app.mailLabels)
	submenu2.add_command(label="Full Contact Info", command=app.noMailLabels)
	
	menubar.add_cascade(label="Edit", menu=filemenu2)
	filemenu2.add_cascade(label='Sort By...', menu=submenu, underline=0)
	filemenu2.add_cascade(label='View', menu=submenu2, underline=0)
	
	root.config(menu=menubar)    
	
	root.minsize(300,300)
	root.geometry("1000x780")
	root.mainloop()  


if __name__ == '__main__':
    main()  