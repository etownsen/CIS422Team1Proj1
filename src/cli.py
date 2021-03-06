"""
	Command-Line Interface module.


	For simple Address Book applet - Project 1 -
	CIS 422, W'14, University of Oregon

	:author: Kevin Beick <kbeick@uoregon.edu>
"""

import sys
from cmd import Cmd

from addressbook import Contact, AddressBook
import utils
import validate

WELCOME_MESSAGE = \
	"\nWelcome to Blue Book!\n" + \
	"Enter \"options\" to view available command options.\n"

OPTIONS_MESSAGE = \
	"VALID COMMANDS:\n" + \
	"add\n" + \
	"edit (flags required to narrow search)\n" + \
	"delete (flags required to narrow search)\n" + \
	"display (flags optional to narrow search)\n" + \
	"display_mail (flags optional to narrow search)\n" + \
	"sort (flags used to define sort criterion; defaults to -ln)\n" + \
	"open\n" + \
	"save\n" + \
	"save_as\n" + \
	"import\n" + \
	"export\n" + \
	"options\n" + \
	"help\n" + \
	"quit\n" + \
	"\n" + \
	"VALID FLAGS (used with commands edit, delete, display, sort):\n" + \
	"NOTE all flags must be followed by a single argument in quotes (eg: -a \"123 Easy St\"; -fn \"Kevin\").\n" + \
	"-fn (first name)\n" + \
	"-ln (last name)\n" + \
	"-a (address)\n" + \
	"-a2 (address line 2)\n" + \
	"-c (city)\n" + \
	"-s (state)\n" + \
	"-z (ZIP Code)\n" + \
	"-p (phone number)\n" + \
	"-e (email)\n"

EDIT_AND_DELETE_NEED_ARGS = \
	"*** This command requires flags and corresponding arguments.\n" + \
	"*** Enter \"options\" to view available command/flag options.\n"

NARROW_SEARCH_MESSAGE = \
	"There are multiple contact that meet those specifications. Find the one you're interested in below\n" + \
	"and add more flags to your command so we can uniquely identify the contact."

BAD_FLAGS_MESSAGE = \
	"*** There's an issue with your flags and/or their arguments.\n" + \
	"*** Make sure you are using valid flags and each flag has a valid, quoted argument.\n" + \
	"*** Enter \"options\" to view available command/flag options.\n"

MALFORMED_DATA_MESSAGE = \
	"*** The contact info you provided does not conform to standards this applet is familiar with.\n" + \
	"*** Please try again."

VALID_OPTIONS = ("add", "edit", "delete", "display", "display_mail", "sort", "open", "save", "save_as", "import", "export", "options", "help", "quit")
VALID_FLAGS = ("-fn", "-ln", "-a", "-a2", "-c", "-s", "-z", "-e")

CONTACT_FIELDS = [
	('fname', 'First Name', '-fn'),
	('lname', '*Last Name', '-ln'),
	('address', 'Address', '-a'),
	('address2', 'Address 2nd Line', '-a2'),
	('city', 'City', '-c'),
	('state', 'State', '-s'),
	('zipcode', 'ZIP Code', '-z'),
	('phone', 'Phone Number', '-p'),
	('email', 'Email', '-e')
]

# Maps fields to validation functions
FIELD_VALIDATORS = {
	'fname' : validate.validate_name,
	'lname' : validate.validate_name,
	'address' : validate.validate_address,
	'address2' : validate.validate_address2,
	'city' : validate.validate_city,
	'state' : validate.validate_state,
	'zipcode' : validate.validate_zip,
	'phone' : validate.validate_phone,
	'email' : validate.validate_email,
}

REQUIRED_FIELDS = [ "lname" ]


def get_field_and_args_from_input(line):
	"""
	Takes 'line' and splits it into [flag, arg] pairs.
	Then validates that flags and arguments are properly formatted, before return a list of 
	corresponding (field, arg) pairs, stored as a list of tuples of strings.
	"""

	line_split_by_quotes = [_ for _ in line.split('"') if _ != '']

	# each flag should have exactly one corresponding arguemnt in quotes
	if len(line_split_by_quotes)%2 != 0   or   line.count('"') != len(line_split_by_quotes)   or   line.count('"') == 0:
	 	print BAD_FLAGS_MESSAGE
	 	return

	flags_args = [[line_split_by_quotes[2*i].strip(), line_split_by_quotes[2*i+1].strip()] 
		for i in range(len(line_split_by_quotes)/2)]

	fields_args = []

	for [flag, arg] in flags_args:
		if flag not in VALID_FLAGS:
			print BAD_FLAGS_MESSAGE
			return

		fields_args.extend([(field[0], arg) for field in CONTACT_FIELDS if flag == field[2]])

	return fields_args


class CommandLineInterface(Cmd):
	"""
	VALID COMMANDS:
	
	| add
	| edit
	| delete
	| display
	| display_mail
	| sort
	| open
	| save
	| save_as
	| import
	| export
	| options
	| help
	| quit

	VALID FLAGS (used with keywords edit, delete, display, sort):
	NOTE all flags must be followed by a single argument in quotes (eg: -a "123 Easy St"; -fn "Kevin").
	-fn (first name)
	-ln (last name)
	-a (address)
	-a2 (address line 2)
	-c (city)
	-s (state)
	-z (ZIP Code)
	-p (phone number)
	-e (email)
	"""

	intro = WELCOME_MESSAGE
	prompt = "> "

	def __init__(self, *args, **kwargs):
		self.addressbook = AddressBook()
		self.current_book_filename = ""
		Cmd.__init__(self, *args, **kwargs)

	def do_add(self, line):
		"""
		Add a new contact to the Address Book.
		"""
		new_contact = Contact()

		print "* denotes a required field.\nPress ctrl-c to cancel."
		for field in CONTACT_FIELDS:
			valid = FIELD_VALIDATORS[field[0]]
			try:
				data = None
				if field[0] in REQUIRED_FIELDS:
					while getattr(new_contact, field[0], '')=='' or not valid(data)[0]:
						data = raw_input("{0}: ".format(field[1]))
						setattr(new_contact, field[0], data)
						if not valid(data)[0]:
							print valid(data)[1]
				else:
					while not valid(data)[0]:
						data = raw_input("{0}: ".format(field[1]))
						setattr(new_contact, field[0], data)
						if not valid(data)[0]:
							print valid(data)[1]
			
			except KeyboardInterrupt:
				print "\nCancelling New Contact\n"
				return

		self.addressbook.add(new_contact)
		print "Your entry was successfully added."

	def do_edit(self, line):
		"""
		Edit an existing contact in the Address Book.
		It actually deletes the "edited " contact and adds a new contact with the changed (or not) fields
		"""
		if line == "":
			print EDIT_AND_DELETE_NEED_ARGS
			return

		# Get list of tuples of (field, arg)
		fields_args = get_field_and_args_from_input(line)
		if not fields_args: return

		# Search address book for specified contact
		lists = [] # a list of lists returned by search, each list the result of a search on one field
		for field_arg in fields_args:
			lists.append(self.addressbook.search(field_arg[0], field_arg[1]))

		# Intersect all resulting lists from field queries
		# This is a list of tuples (index, contact)
		search_results = list(set(lists[0]).intersection(*lists[1:]))

		# if more than one such contact, display list of said contacts
		# if exacly one such contact, that is the one we want
		# if no such contact, inform user
		if len(search_results) > 1:
			print NARROW_SEARCH_MESSAGE
			for result in search_results:
				print "-------------------------"
				print result[1]

		elif len(search_results) == 1:
			print "\nPress ctrl-c to cancel."

			contact = search_results[0] #tuple (index, contact)

			# TODO, create temp contact to hold edits, replace old contact with new
			temp = Contact()

			for field in CONTACT_FIELDS:
				valid = FIELD_VALIDATORS[field[0]]
				try:
					new_data = None
					old_data = getattr(contact[1], field[0], '')
					while not valid(new_data)[0]:
						user_input = raw_input("{0}: {1}".format(field[1], old_data) + chr(8)*len(old_data))
						# NOTE: 8 is the ASCII value of backspace
						if not user_input:
							user_input = old_data

						# My hacky way of having the newly added chars replace those of the old_data
						# for cases where user replaces some, but not all, of the old data's chars
						user_input = list(user_input)
						new_data = list(old_data)
						for i in range(len(user_input)):
							try:
								new_data[i] = user_input[i]
							except IndexError:
								new_data.extend(user_input[i:])
								break
						new_data = ''.join(new_data)
						if not valid(new_data)[0]:
							print valid(new_data)[1]

					# Update the temp Contact Info
					setattr(temp, field[0], new_data)
			
				except KeyboardInterrupt:
					print "\nCancelling Contact Edit, reverting to original.\n"
					return

			confirm = raw_input("Are you sure you want to make these changes to this entry? (y/n): ")
			if confirm in ('yes', 'y'):
				self.addressbook.delete(contact[0])
				self.addressbook.add(temp)
				print "Edit complete"
				return

			else:
				print "\nCancelling Contact Edit, reverting to original.\n"


		else:
			print "There were no contacts that met your specification. Please generalize your request."

	def do_delete(self, line):
		"""
		Deletes a contact from the Address Book.
		Or if more than one contact meets the user's specification, presents a list of said contacts.
		If no contacts meet the user's specification, then does nothing.
		**User can only delete one contact at a time.**
		"""
		if line == "":
			print EDIT_AND_DELETE_NEED_ARGS
			return

		# Get list of tuples of (field, arg)
		fields_args = get_field_and_args_from_input(line)
		if not fields_args: return

		# Search address book for specified contact
		lists = [] # a list of lists returned by search, each list the result of a search on one field
		for field_arg in fields_args:
			lists.append(self.addressbook.search(field_arg[0], field_arg[1]))

		# Intersect all resulting lists from field queries
		# This is a list of tuples (index, contact)
		search_results = list(set(lists[0]).intersection(*lists[1:]))

		# if more than one such contact, display list of said contacts
		# if exacly one such contact, that is the one we want
		# if no such contact, inform user
		if len(search_results) > 1:
			print NARROW_SEARCH_MESSAGE
			for result in search_results:
				print "-------------------------"
				print result[1]

		elif len(search_results) == 1:
			contact = search_results[0] #tuple (index, contact)
			print contact[1]
			yes_delete = raw_input("Is this the entry you want to delete? (y/n): ")
			if yes_delete in ('yes', 'y'):
				yes_delete = raw_input("*** Are you sure? (y/n): ")
				if yes_delete in ('yes', 'y'):
					try:
						self.addressbook.delete(contact[0])
						print "Contact deleted."
					except:
						print "*** Encountered an error while trying to delete, please make sure your input is correct."
					return
			print "No deletions."
		else:
			print "There were no contacts that met your specification. Please generalize your request."

	def do_display(self, line):
		"""
		If no flags are given, displays all contacts in the Address Book.
		If flags are present, then displays only contacts that meet all of the specifications given by flags.
		"""

		if self.addressbook.total == 0:
			print "The addressbook is empty."
			return

		# if no flags, arguments: 
		# Print entire address book
		if line == '':
			print "\n{0}".format(self.addressbook)

		# else find subset of addressbook
		else:
			# Get list of tuples (field, arg)
			fields_args = get_field_and_args_from_input(line)
			if not fields_args: return

			# Search address book for specified contacts
			lists = [] # a list of lists returned by search, each list the result of a search on one field
			for field_arg in fields_args:
				lists.append(self.addressbook.search(field_arg[0], field_arg[1]))

			# Intersect all resulting lists from field queries
			# This is a list of tuples (index, contact)
			search_results = list(set(lists[0]).intersection(*lists[1:]))

			if len(search_results) > 0:
				for result in search_results:
					print "\n{0}".format(result[1])
				print "\n"
			else:
				print "There were no contacts that met your specification. Please generalize/check your request."

	def do_display_mail(self, line):
		"""
		Same as 'display', but displays contact in mailing label format, as opposed to full contact.
		If no flags are given, displays all contacts in the Address Book.
		If flags are present, then displays only contacts that meet all of the specifications given by flags.
		"""

		if self.addressbook.total == 0:
			print "The addressbook is empty."
			return

		# if no flags, arguments: 
		# Print entire address book
		if line == '':
			print "\n{0}".format(self.addressbook.print_all_mailing())

		# else find subset of addressbook
		else:
			# Get list of tuples (field, arg)
			fields_args = get_field_and_args_from_input(line)
			if not fields_args: return

			# Search address book for specified contacts
			lists = [] # a list of lists returned by search, each list the result of a search on one field
			for field_arg in fields_args:
				lists.append(self.addressbook.search(field_arg[0], field_arg[1]))

			# Intersect all resulting lists from field queries
			# This is a list of tuples (index, contact)
			search_results = list(set(lists[0]).intersection(*lists[1:]))

			if len(search_results) > 0:
				for result in search_results:
					print "\n{0}".format(result[1].print_mailing())
				print "\n"
			else:
				print "There were no contacts that met your specification. Please generalize/check your request."
	
	def do_sort(self, line):
		"""
        Sort the address book by the given attributes (flags). The first
        attribute is used and ties are broken using the following attributes in
        the list.
        Defaults to sorting by last name.  Ties are broken by last name.
		"""

		# convert flags to list of attributes.
		flags = line.split()
		attrs = []

		for flag in flags:
			if flag not in VALID_FLAGS:
				print "'{0}' is not a valid flag. Enter \"options\" to view available flag options.\n".format(flag)
				return

			for field in CONTACT_FIELDS:
				if flag == field[2]:
					attrs.append(field[0])

		# Ties are broken by name
		attrs.extend(['lname', 'fname'])

		# Apply sort function
		try:
			self.addressbook.sort(attributes=attrs)
			print "Address book is now sorted.\n"
		except:
			print "*** Encountered an error while trying to sort, please make sure your input is correct."

	def do_open(self, line):
		"""
		Open an address book from file.
		"""

		confirm = raw_input("Are you sure you want to open a new address book? Changes since your last save will be lost. ('open' / 'cancel'): ")
		if confirm != 'open': return		

		file_name = raw_input("Please give the name/path of the file containing the address book you want to open (or leave blank to cancel): ")

		if file_name:
			try:
				self.addressbook = utils.open_addressbook(file_name)
				self.current_book_filename = file_name
				print "Now using address book from file '{0}'".format(file_name)
			except:
				print "*** Encountered an error while trying to open that file. Please make sure you provided a good file name."

	def do_save(self, line):
		"""
		Save an address book as an object to a file, to the file name inferred from current address book.
		"""

		if self.current_book_filename == '': 
			print "This seems to be a new address book."
			return self.do_save_as(line)


		file_name = self.current_book_filename

		confirm = raw_input("Are you sure you want to overwrite the existing file '{0}'? (y/n): ".format(file_name))
		if confirm in ['yes', 'y']:
			try:
				utils.save_addressbook(self.addressbook, file_name)
				print "Successfully saved your address book to the file '{0}'".format(file_name)
			except:
				print "in save"
				print "*** Encountered an error while trying to save. Sorry..."

		else:
			print "Cancelling save."
			return

	def do_save_as(self, line):
		"""
		Save an address book as an object to a file.
		"""

		file_name = raw_input("What do you want to call your file? (or leave blank to cancel): ")
			# "WARNING, I can't tell if you're overwritting a file that already exists, so choose the name carefully: ")

		if not file_name: return

		try:
			with open(file_name):
				overwrite = raw_input("There already seems to be a file with that name. Do you want to overwrite that file? (y/n): ")
		except IOError:
			overwrite = 'yes'

		if overwrite in ['yes', 'y']:
			try:
				utils.save_addressbook(self.addressbook, file_name)
				self.current_book_filename = file_name
				print "Successfully saved your address book to the file '{0}'".format(file_name)
			except:
				print "in save as"
				print "*** Encountered an error while trying to save. Sorry..."
	
	def do_import(self, line):
		"""
		Import a contacts list from a tsv file and add the contacts to the current book.
		The format of the file is as follows:
		
		| Last<tab>Delivery<tab>Second<tab>Recipient<tab>Phone<NL>
		| followed by a list of contacts with the same format.
		"""
		file_name = raw_input("Please give the name/path of the file from which you want to import contacts (or leave blank to cancel): ")

		if file_name:
			confirm = raw_input("Are you sure you want to try to merge the contacts from this file into your current book? (y/n): ")
			if confirm not in ['yes', 'y']: print "Cancelling import."; return
			try:
				self.addressbook.import_contacts(file_name)
				print "Successfully imported contacts from '{0}'".format(file_name)
			except:
				print "*** Encountered an error while trying to import from that file. " + \
					"Please make sure you provided a good file name and that the file matches the format described in 'help import'."
		else:
			print "Cancelling import."

	def do_export(self, line):	
		"""
		Export the contacts of the current AddressBook to a tsv file.
		The format of the file is as follows:
		
		| Last<tab>Delivery<tab>Second<tab>Recipient<tab>Phone<NL>
		| followed by a list of contacts with the same format.
		"""	
		file_name = raw_input("Please give the name of the file to which you want to export contacts (or leave blank to cancel): ")
			
		if file_name:
			try:
				self.addressbook.export_contacts(file_name)
				print "Successfully exported your address book to the file '{0}'".format(file_name)
			except:
				print "*** Encountered an error while trying to export. Sorry..."
		else:
			print "Cancelling export."


	def do_options(self, line):
		"""
		Displays the available keyword commands and flags used by the applet.
		"""
		print OPTIONS_MESSAGE

	def do_quit(self, line):
		"""
		quit the applet
		"""
		confirm = raw_input("Are you sure you want to quit? Changes since your last save will be lost. ('quit' to quit; anything else will cancel): ")
		if confirm != 'quit': 
			return
		else:
			sys.exit()

	def default(self, line):
		"""
		Method called on an input line when the command prefix is not recognized.
		"""
		if line != "":
			print "*** Invalid command.  Type \"options\" to view available command options."

	def emptyline(self):
		"""
		Method called when an empty line is entered in response to the prompt.
		If this method is not overridden, it repeats the last nonempty command entered.
		"""
		pass
 

if __name__ == "__main__":
	command = CommandLineInterface()
	command.cmdloop()
