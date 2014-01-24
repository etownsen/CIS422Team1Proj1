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
	"Type \"help\" to view available command options.\n"

OPTIONS_MESSAGE = \
	"VALID KEYWORDS:\n" + \
	"add\n" + \
	"edit\n" + \
	"delete\n" + \
	"display\n" + \
	"quit\n" + \
	"options\n" + \
	"help\n\n" + \
	\
	"VALID FLAGS (used with keywords edit, delete, display):\n" + \
	"-fn (first name)\n" + \
	"-ln (last name)\n" + \
	"-a (address)\n" + \
	"-c (city)\n" + \
	"-s (state)\n" + \
	"-z (ZIP Code)\n" + \
	"-e (email)\n"


class CommandLineInterface(Cmd):

	"""
	VALID KEYWORDS:
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
	-fn (first name)
	-ln (last name)
	-a (address)
	-c (city)
	-s (state)
	-z (ZIP Code)
	-e (email)

	"""

	intro = WELCOME_MESSAGE

	options = ("add", "edit", "delete", "display", "quit", "options")
	flags = ("-fn", "-ln", "-a", "-c", "-s", "-z", "-e")


	def do_options(self, line):
		"""
		Displays the available keyword commands used by the applet.
		"""
		print OPTIONS_MESSAGE

	def do_quit(self, line):
		"""
		quit the applet
		"""
		print "\n"
		sys.exit()



if __name__ == "__main__":
	command = CommandLineInterface()
	command.cmdloop()

