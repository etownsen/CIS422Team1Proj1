"""
	Command-Line Interface module.


	For simple Address Book applet - Project 1 -
	CIS 422, W'14, University of Oregon

	:author: Kevin Beick <kbeick@uoregon.edu>
"""

import sys
from cmd import Cmd

from addressbook import Contact, AddressBook

WELCOME_MESSAGE = \
	"\nWelcome to Blue Book!\n" + \
	"Enter \"options\" to view available command options.\n"

OPTIONS_MESSAGE = \
	"VALID COMMANDS:\n" + \
	"add\n" + \
	"edit (flags required to narrow search)\n" + \
	"delete (flags required to narrow search)\n" + \
	"display (flags optional to narrow search)\n" + \
	"quit\n" + \
	"options\n" + \
	"help\n\n" + \
	\
	"VALID FLAGS (used with commands edit, delete, display):\n" + \
	"NOTE all flags must be followed by a single argument in quotes (eg: -a \"123 Easy St\"; -fn \"Kevin\").\n" + \
	"-fn (first name)\n" + \
	"-ln (last name)\n" + \
	"-a (address)\n" + \
	"-c (city)\n" + \
	"-s (state)\n" + \
	"-z (ZIP Code)\n" + \
	"-e (email)\n"

EDIT_AND_DELETE_NEED_ARGS = \
	"***This command requires flags and corresponding arguments.\n" + \
	"***Enter \"options\" to view available command/flag options.\n"

NARROW_SEARCH_MESSAGE = \
	"There are multiple contact that meet those specifications. Find the one you're interested in below\n" + \
	"and add more flags to your command so we can uniquely identify the contact."

BAD_FLAGS_MESSAGE = \
	"***There's an issue with your flags and/or their arguments.\n" + \
	"***Make sure you are using valid flags and each flag has a valid, quoted argument.\n" + \
	"***Enter \"options\" to view available command/flag options.\n"

VALID_OPTIONS = ("add", "edit", "delete", "display", "quit", "options", "help")
VALID_FLAGS = ("-fn", "-ln", "-a", "-c", "-s", "-z", "-e")

CONTACT_FIELDS = [
	('fname', 'First Name', '-fn'),
	('lname', '*Last Name', '-ln'),
	('address', 'Address', '-a'),
	('city', 'City', '-c'),
	('state', 'State', '-s'),
	('zipcode', 'ZIP Code', '-z'),
	('phone', 'Phone Number', '-p'),
	('email', 'Email', '-e')
]

REQUIRED_FIELDS = [ "lname" ]

def even_num_words(line):
	"""
	returns true if 'line' consists of an even number of white-spaced even_num_words
	returns false otherwise
	"""
	return len(str.split(line))%2 == 0

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
	add
	edit
	delete
	display
	quit
	options
	help

	TODO: 
	import
	export

	VALID FLAGS (used with keywords edit, delete, display):
	NOTE all flags must be followed by a single argument in quotes (eg: -a "123 Easy St"; -fn "Kevin").
	-fn (first name)
	-ln (last name)
	-a (address)
	-c (city)
	-s (state)
	-z (ZIP Code)
	-e (email)

	"""

	intro = WELCOME_MESSAGE
	prompt = "> "

	def __init__(self, *args, **kwargs):
		self.addressbook = AddressBook()
		Cmd.__init__(self, *args, **kwargs)

	def do_prepop_book(self, line):
		# TODO this is for testing, should be removed for final product
		a = Contact('aaa', 'AAA', '10 a st', 'Eugene', 'OR', '97401', '541', 'a@a.com')
		b = Contact('bbb', 'BBB', '20 b st', 'Eugene', 'OR', '97402', '541', 'b@b.com')
		c = Contact('ccc', 'CCC', '30 c st', 'Eugene', 'OR', '97403', '541', 'c@c.com')
		self.addressbook.add([a, b, c])

	def do_add(self, line):
		"""
		Add a new contact to the Address Book.
		"""
		new_contact = Contact()

		print "* denotes a required field.\nPress ctrl-c to cancel."
		for field in CONTACT_FIELDS:
			try:
				#***TODO, Validate input as correctly formatted
				if field[0] in REQUIRED_FIELDS:
					while getattr(new_contact, field[0], '')=='':
						setattr(new_contact, field[0], raw_input("{0}: ".format(field[1])))
				else:
					setattr(new_contact, field[0], raw_input("{0}: ".format(field[1])))
			
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

		# # There should be a one-to-one correspondence between flags and arguments
		# if not even_num_words(line):
		# 	print BAD_FLAGS_MESSAGE
		# 	return

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
				try:
					old_data = getattr(contact[1], field[0], '')
					user_input = raw_input("{0}: {1}".format(field[1], old_data) + chr(8)*len(old_data))
					# NOTE: 8 is the ASCII value of backspace
					if not user_input:
						user_input = old_data

					# Update the temp Contact Info
					setattr(temp, field[0], user_input)
			
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

		# # There should be a one-to-one correspondence between flags and arguments
		# if not even_num_words(line):
		# 	print BAD_FLAGS_MESSAGE
		# 	return

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
				yes_delete = raw_input("***Are you sure? (y/n): ")
				if yes_delete in ('yes', 'y'):
					self.addressbook.delete(contact[0])
					print "Contact deleted."
					return
			print "No deletions."

		else:
			print "There were no contacts that met your specification. Please generalize your request."



	def do_display(self, line):
		"""
		If no flags are given, displays all contacts in the Address Book.
		If flags are present, then displays only contacts that meet all of the specifications given by flags.
		"""

		# # There should be a one-to-one correspondence between flags and arguments
		# if not even_num_words(line):
		# 	print BAD_FLAGS_MESSAGE
		# 	return

		# if no flags, arguments: 
		# Print entire address book
		if line == '':
			if self.addressbook.total == 0:
				print "The addressbook is empty"
			else:
				print self.addressbook

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
					print "-------------------------"
					print result[1]
			else:
				print "There were no contacts that met your specification. Please generalize/check your request."


	def do_options(self, line):
		"""
		Displays the available keyword commands and flags used by the applet.
		"""
		print OPTIONS_MESSAGE

	def do_quit(self, line):
		"""
		quit the applet
		"""
		print ""
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
