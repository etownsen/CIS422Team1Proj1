"""
	Command-Line Interface module
	For simple Address Book applet - Project 1 - CIS 422, W'14, University of Oregon

	:author: Kevin Beick
"""

import sys
from cmd import Cmd

# TODO import dependencies from backend

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

BAD_FLAGS_MESSAGE = \
	"***There's an issue with your flags and/or their arguments.\n" + \
	"***Make sure you are using valid flags and each flag has a valid argument.\n" + \
	"***Enter \"options\" to view available command/flag options.\n"

VALID_OPTIONS = ("add", "edit", "delete", "display", "quit", "options", "help")
VALID_FLAGS = ("-fn", "-ln", "-a", "-c", "-s", "-z", "-e")

CONTACT_FIELDS = [
	('fname', 'First Name'),
	('lname', 'Last Name'),
	('address', 'Address'),
	('city', 'City'),
	('state', 'State'),
	('zip', 'ZIP Code'),
	('phone', 'Phone Number'),
	('email', 'Email')
]

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

	line_tuples = [(split_line[2*i].strip('\"'), split_line[2*i+1].strip('\"')) 
		for i in range(len(split_line)/2)]

	for (flag, arg) in line_tuples:
		if flag not in VALID_FLAGS:
			print BAD_FLAGS_MESSAGE
			return

		print "{0}::{1}".format(flag,arg)

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


	def do_add(self, line):
		"""
		Add a new contact to the Address Book.
		"""
		#***TODO, make a new contact object

		for field in CONTACT_FIELDS:
			
			#***TODO, assign raw input to proper field of contact
			#***TODO, Validate input as correctly formatted
			print raw_input("{0}: ".format(field[1]))

		#*** TODO, add new contact to Address Book
		#***TODO, print "Your entry was successfully added."
		print "TODO"


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

		flag_args = parse_line_to_flags_args(line)

		#***TODO, search address book for specified contact

		# if more than one such contact, display list of said contacts
		# if exacly one such contact, that is the one we want
		default = "Jackmans"
		# if no such contact, inform user

		#***TODO, 
		for field in CONTACT_FIELDS:
			user_input = raw_input("{0}: {1}".format(field[1], default) + chr(8)*len(default))
			# NOTE: 8 is the ASCII value of backspace
			if not user_input:
				user_input = default

		print "TODO"


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

		flag_args = parse_line_to_flags_args(line)

		#***TODO, search address book for specified contact

		# if more than one such contact, display list of said contacts
		# if exacly one such contact, that is the one we want
			#***TODO, remove said 
		# if no such contact, inform user

		print "TODO"


	def do_display(self, line):
		"""
		If no flags are given, displays all contacts in the Address Book.
		If flags are present, then displays only contacts that meet all of the specifications given by flags.
		"""

		# There should be a one-to-one correspondence between flags and arguments
		if not even_num_words(line):
			print BAD_FLAGS_MESSAGE
			return

		flag_args = parse_line_to_flags_args(line)

		#***TODO, search address book for specified contact

		# Print list of found contacts

		print "TODO"


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
