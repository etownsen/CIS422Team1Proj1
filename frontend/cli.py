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
	"Type \"options\" to view available command options.\n"

OPTIONS_MESSAGE = \
	"VALID COMMANDS:\n" + \
	"add\n" + \
	"edit\n" + \
	"delete\n" + \
	"display\n" + \
	"quit\n" + \
	"options\n" + \
	"help\n\n" + \
	\
	"VALID FLAGS (used with keywords edit, delete, display):\n" + \
	"(all flags must be followed by a single argument)\n" + \
	"-fn (first name)\n" + \
	"-ln (last name)\n" + \
	"-a (address)\n" + \
	"-c (city)\n" + \
	"-s (state)\n" + \
	"-z (ZIP Code)\n" + \
	"-e (email)\n"

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


class CommandLineInterface(Cmd):
	"""
	VALID COMMANDS:
	add
	edit
	delete
	display
	quit
	options

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

	options = ("add", "edit", "delete", "display", "quit", "options", "help")
	flags = ("-fn", "-ln", "-a", "-c", "-s", "-z", "-e")


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

		#***TODO, isolate flags, arguments
		#***TODO, search address book for specified contact
		#***TODO, 
		for field in CONTACT_FIELDS:
			default = "Jackmans"
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
		print "TODO"


	def do_display(self, line):
		"""
		If no flags are given, displays all contacts in the Address Book.
		If flags are present, then displays only contacts that meet all of the specifications given by flags.
		"""
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

