"""
	Command-Line Interface module
	For simple Address Book applet - Project 1 - CIS 422, W'14, University of Oregon

	:author: Kevin Beick
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
	"(each and every flags must be followed by a single argument)\n" + \
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
	"***Make sure you are using valid flags and each flag has a valid argument.\n" + \
	"***Enter \"options\" to view available command/flag options.\n"

VALID_OPTIONS = ("add", "edit", "delete", "display", "quit", "options", "help")
VALID_FLAGS = ("-fn", "-ln", "-a", "-c", "-s", "-z", "-e")

CONTACT_FIELDS = [
	('fname', 'First Name', '-fn'),
	('lname', 'Last Name', '-ln'),
	('address', 'Address', '-a'),
	('city', 'City', '-c'),
	('state', 'State', '-s'),
	('zipcode', 'ZIP Code', '-z'),
	('phone', 'Phone Number', '-p'),
	('email', 'Email', 'e')
]

REQUIRED_FIELDS = [ "lname" ]

def even_num_words(line):
	"""
	returns true if 'line' consists of an even number of white-spaced even_num_words
	returns false otherwise
	"""
	return len(str.split(line))%2 == 0

def parse_line_to_flags_args(line):
	"""
	Takes 'line' and splits it into pairs of tokens, stored as a list of tuples of strings.
	Then validates that flags and arguments are properly formatted.
	"""
	split_line = str.split(line)

	line_pairs = [[split_line[2*i].strip('\"'), split_line[2*i+1].strip('\"')] 
		for i in range(len(split_line)/2)]

	line_tuples = []

	for [flag, arg] in line_pairs:
		if flag not in VALID_FLAGS:
			print BAD_FLAGS_MESSAGE
			return

		line_tuples.extend([(field[0], arg) for field in CONTACT_FIELDS if flag == field[2]])

	return line_tuples


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
	(all flags must be followed by a single argument)
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
		a = Contact('aaa', 'AAA', '10 a st', 'Eugene', 'OR', '97401', '541', 'a@a.com')
		b = Contact('bbb', 'BBB', '20 b st', 'Eugene', 'OR', '97402', '541', 'b@b.com')
		c = Contact('ccc', 'CCC', '30 c st', 'Eugene', 'OR', '97403', '541', 'c@c.com')
		self.addressbook.add([a, b, c])

	def do_add(self, line):
		"""
		Add a new contact to the Address Book.
		"""
		new_contact = Contact()

		print "* denotes a required field"
		for field in CONTACT_FIELDS:
			
			#***TODO, Validate input as correctly formatted
			if field[0] in REQUIRED_FIELDS:
				while getattr(new_contact, field[0], '')=='':
					setattr(new_contact, field[0], raw_input("*{0}: ".format(field[1])))
			else:
				setattr(new_contact, field[0], raw_input("{0}: ".format(field[1])))

		self.addressbook.add(new_contact)
		print "Your entry was successfully added."

	def do_edit(self, line):
		"""
		Edit an existing contact in the Address Book.
		"""
		if line == "":
			print EDIT_AND_DELETE_NEED_ARGS
			return

		# There should be a one-to-one correspondence between flags and arguments
		if not even_num_words(line):
			print BAD_FLAGS_MESSAGE
			return

		# Get list of tuples of (field, arg)
		field_args = parse_line_to_flags_args(line)

		# Search address book for specified contact
		lists = [] # a list of lists returned by search, each list the result of a search on one field
		for field_arg in field_args:
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
			print "*You cannot undo changes once you move to next field; be careful."
			contact = search_results[0][1]
			for field in CONTACT_FIELDS:
				old_data = getattr(contact, field[0], '')
				user_input = raw_input("{0}: {1}".format(field[1], old_data) + chr(8)*len(old_data))
				# NOTE: 8 is the ASCII value of backspace
				if not user_input:
					user_input = old_data

				# Update the Contact Info
				setattr(contact, field[0], user_input)
			print "Edit complete"

		else:
			print "There were no contacts that met your specification. Please generalize your request."


	def do_delete(self, line):
		"""
		Deletes a contact from the Address Book.
		Or if more than one contact meets the user's specification, presents a list of said contacts.
		If no contacts meet the user's specification, then does nothing.
		*User can only delete one contact at a time
		"""
		if line == "":
			print EDIT_AND_DELETE_NEED_ARGS
			return

		# There should be a one-to-one correspondence between flags and arguments
		if not even_num_words(line):
			print BAD_FLAGS_MESSAGE
			return

		# Get list of tuples of (field, arg)
		field_args = parse_line_to_flags_args(line)

		# Search address book for specified contact
		lists = [] # a list of lists returned by search, each list the result of a search on one field
		for field_arg in field_args:
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

		# There should be a one-to-one correspondence between flags and arguments
		if not even_num_words(line):
			print BAD_FLAGS_MESSAGE
			return

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
			field_args = parse_line_to_flags_args(line)

			# Search address book for specified contacts
			lists = [] # a list of lists returned by search, each list the result of a search on one field
			for field_arg in field_args:
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