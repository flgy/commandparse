#!/usr/bin/env python3

from argparse import ArgumentParser
from commandparse import Command


class Example(Command):

	# Can have arbitrary arguments
	def __init__(self):
		pass

	def get_info(self, kwargs):
		"""
		Return infos.

		Arguments:
			#arg:string
				Positional argument
			@option:string = "default_option"
				Optional argument with default value
			@verbose:bool
				Verbose mode
		"""
		arg = kwargs.get("arg", "default_value")
		option = kwargs.get("option", "default_option_2")
		verbose = kwargs.get("verbose", False)
		# do stuff with info
		if verbose:
			print("verbose")

		print(arg)
		print(option)


if __name__ == "__main__":

	parser = ArgumentParser()
	sub = parser.add_subparsers(title="commands", dest="command", description="available commands")

	commands = {}
	for command, method in Example.get_commands(prefix="get_"):
		Example.set_subparser_for(command, method, sub)
		commands[command] = method

	args = parser.parse_args()

	if args.command:
		example = Example()
		example.dispatch_command(commands, args)
	else:
		parser.print_usage()
