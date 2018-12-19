"""
@author: flgy

Module to parse command based CLI application.

Usage:
	* Subclass the Command class
	* Add a method with a name such as `prefix_commandname` with kwargs as required argument
	* Create a an ArgumentParser and declare a subparser per command
	* Register the commands in a dictionary
	* Use the dispatch_command function with the commands and args returned by `parser.parse_args()`

parser = ArgumentParser(...)
[...]
sub = parser.add_subparsers(title="commands", dest="command", description="available commands")

# Registering commands
commands = {}
for command, method in Subclass.get_commands(prefix="prefix_"):
	Subclass.set_subparser_for(command, method, sub)
	commands[command] = method
[...]
args = parser.parse_args()

if args.command:
	cmd = Subclass(...)
	cmd.dispatch_command(commands, args)
else:
	parser.print_usage()
"""

from ast import literal_eval
from inspect import getmembers
from re import findall

class CommandTypeError(Exception):
	pass

class CommandDefaultValueError(Exception):
	pass

class Command():

	TYPES = {
		"string": str,
		"int": int,
		"float": float,
		"bool": bool,
		"list": list
	}

	@staticmethod
	def __parse_docstring(docstring):
		"""
		Parse a docstring to extract help and argument to generate a subparsers with arguments.
		The expected format is (triple quotes are replaced by { and }):

			{{{
			Help line

			Arguments:
				@argumentName:argumentType
				@argumentName:argumentType = value
				#argumentName:argumentType
				#argumentName:argumentType = value
			}}}

		@ means an optional argument that is not required.
		# means a positional argument (should have a value if it's a not required option).
		value can take one argument: like `value` or multiple values with a list syntax: `['foo', 'bar']`.
		"""
		result = {}
		lines = docstring.replace("\t", "").split("\n")
		help_line = ""
		arguments = {}

		s_argument = False
		while lines != []:
			line = lines.pop(0).strip()

			if line.strip() == "":
				continue

			else:
				if not s_argument:
					if line == "Arguments:":
						s_argument = True
					else:
						help_line += " " + line
				else:
					if line[0] in ["@", "#"]:
						opt = line[0]
						arg = line[1:]
						variable, _, values = arg.partition(" = ")
						name, _, typ = variable.partition(':')

						if typ in Command.TYPES:
							typ = Command.TYPES[typ]
						else:
							raise CommandTypeError("{typ} not supported by commandparse".format(typ))

						alias = name[0]
						arguments[name] = {
							"alias": "-{alias}".format(alias=alias),
							"name": "--{name}".format(name=name),
							"type": typ,
							"help_line": "",
						}
						if values:
							try:
								v = literal_eval(values)
							except ValueError:
								raise CommandDefaultValueError("Incorret value(s) in a placeholder: {v}".format(v=values))
							if isinstance(v, list):
								arguments[name]["values"] = v
							elif isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
								arguments[name]["value"] = v

						if opt == "#":
							arguments[name]["pos"] = True
						elif opt == "@":
							arguments[name]["pos"] = False

					elif line:  # if no prefix is found, read the help line of the previous argument.
						if not arguments[name]["help_line"]:
							arguments[name]["help_line"] = line
						else:
							arguments[name]["help_line"] += " " + line

		return {"help_line": help_line.strip(), "arguments": arguments}

	@classmethod
	def get_commands(cls, prefix=""):
		"""
		Iterator yielding object methods with

		:prefix: filter object methods to return
		"""
		parent_members = [k for k, v in getmembers(Command)]
		for method, func in getmembers(cls):
			if callable(func) and method not in parent_members and method.startswith(prefix):
					command = findall("{}_?(.*)".format(prefix), method)[0]
					yield (command, method)

	@classmethod
	def set_subparser_for(cls, command, method, subparser):
		"""
		Take a subparser as argument and add arguments corresponding to command in it.

		:command: name to display in the help
		:method: function name corresponding to the command
		:subparser: subparser object to add argument(s) to
		"""
		func = getattr(cls, method)
		args_info = cls.__parse_docstring(func.__doc__)
		c = subparser.add_parser(command, help=args_info["help_line"])

		if "arguments" in args_info:
			for label, arg in args_info["arguments"].items():
				if arg["pos"]:
					if arg["type"] == bool:
						raise CommandTypeError("bool type not supported as positional argument")
					if "value" in arg:
						if arg["type"] in [str, int, float]:
							c.add_argument(label, nargs='?', default=arg["value"], type=arg["type"], help=arg["help_line"])
					elif "values" in arg:
						if arg["type"] in [str, int, float]:
							c.add_argument(label, nargs='?', default=arg["values"][0], choices=arg["values"], type=arg["type"], help=arg["help_line"])
						elif arg["type"] == list:
							c.add_argument(label, nargs='+', default=arg["values"][0], choices=arg["values"], help=arg["help_line"])
					else:
						c.add_argument(label, type=arg["type"], help=arg["help_line"])
				else:
					if arg["type"] == bool:
						c.add_argument(arg["alias"], arg["name"], action="store_true", default=False, help=arg["help_line"])
					elif arg["type"] in [str, int, float] and "value" in arg:
						c.add_argument(arg["alias"], arg["name"], type=arg["type"], default=arg["value"], help=arg["help_line"])
					elif arg["type"] == list and "values" not in arg:
						c.add_argument(label, nargs="*", help=arg["help_line"])
					elif "values" in arg:
						if arg["type"] == list:
							c.add_argument(label, choices=arg["values"], default=arg["values"][0], nargs="*", help=arg["help_line"])
						else:
							c.add_argument(label, type=arg["type"], choices=arg["values"], default=arg["values"][0], nargs="?", help=arg["help_line"])
					else:
						c.add_argument(arg["alias"], arg["name"], type=arg["type"], help=arg["help_line"])

	def has_option(self, method, option):
		"""
		Return `true` if a given method has a certain option.

		:method: method name to search for the option
		:option: the option to search in the method

		Option also means argument.
		"""
		args = self.__parse_docstring(getattr(self, method).__doc__)
		if "arguments" in args:
			return any(option == label for label in args["arguments"].keys())
		return False

	def retrieve_default_val_for_arg(self, method, argname):
		"""
		Return the default value(s) of a certain argument/option of a given method.

		:method: method name to retrieve argument value(s)
		:argname: argument to return default value(s)
		"""
		args = self.__parse_docstring(getattr(self, method).__doc__)
		if "arguments" in args:
			arguments = args["arguments"]
		if argname in arguments and "value" in arguments[argname] or "values" in arguments[argname]:
			return arguments[argname]["value"] if "value" in arguments[argname] else arguments[argname]["values"]
		else:
			return None

	def dispatch_command(self, commands_dict, command, args):
		"""
		Execute the corresponding command with provided args.

		:commands: dictionary containing subclass methods, hashed by command name (may be method suffix).
		:command: string containing the command
		:args: result from ArgumentParser.parse_args()
		"""
		getattr(self, commands_dict[command])(vars(args))

