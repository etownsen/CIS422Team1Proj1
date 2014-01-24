"""
	Command-Line Interface module
	For simple Address Book applet - Project 1 - CIS 422, W'14, University of Oregon

	:author: Kevin Beick
"""

from cmd import Cmd

# TODO import dependencies from backend



class CommandLineInterface(Cmd):

	"""
	VALID KEYWORDS:
	add
	edit
	delete
	display
	quit
	help

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

	intro = "\nWelcome to Blue Book!\n" + \
			"Type \"help\" to view available command options.\n"

	options = ("add", "edit", "delete", "display", "quit", "help")
	flags = ("-fn", "-ln", "-a", "-c", "-s", "-z", "-e")



if __name__ == "__main__":
	command = CommandLineInterface()
	command.cmdloop()