"""
@author: flgy

Module to parse command based CLI application.

Usage:
	* Subclass the Command class
	* Add a method with a name such as `prefix_commandname` with kwargs as required argument
	* Create an ArgumentParser instance
	* Call the `Subclass.add_suparsers` with the ArgumentParser instance and other settings
	* Use the `dispatch_command` function with the args returned by `parser.parse_args()`

parser = ArgumentParser(...)
[...]
cmd.add_subparsers(parser, prefixes=["get_", ...], delim="_", title="commands", description="available commands")
cmd = Subclass(...)
cmd.dispatch_command(commands, args)
"""

from ast import literal_eval
from inspect import getmembers
from re import findall
from uuid import uuid4
from argparse import ArgumentError


class CommandTypeError(Exception):
	pass


class CommandDefaultValueError(Exception):
	pass


class CommandNotFoundError(Exception):
	pass


class CommandParserNameDuplicated(Exception):
	pass

class Command():

	TYPES = {
		"string": str,
		"int": int,
		"float": float,
		"bool": bool,
		"list": list
	}
	COMMANDS = {}

	@staticmethod
	def __parse_docstring(docstring):
		"""
		Parses a docstring to extract help and argument to generate a subparsers with arguments.
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
		if docstring is None or docstring == "":
			return {}
		lines = docstring.replace("\t", "").split("\n")
		result = {}
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
	def add_subparsers(cls, parser, name="", prefixes=[], delim="_", title="commands", description="available commands", required=True):
		"""
		Parse the calling classes and extract commands, for each command register a subparser.
	
		:cls: class to register subparsers
		:parser: add the subparsers to the provided parser
		:prefixes: str list of prefixes corresponding to command methods
		:delim: str delimiter to separate prefix from commnad name
		:title: title of the subparser
		:description: description of the subparser
		"""
		command = f"command_{name}"
		if command in cls.COMMANDS:
			raise CommandParserNameDuplicated(f"Command parser with name {name} already registered.")
		
		cls.COMMANDS[command] = {}
		
		sub = parser.add_subparsers(title=title, dest=command, description=description)
		sub.required = True
		for pf in prefixes:
			for c, method in cls.get_commands(prefix=pf, delim=delim):
				cls.set_subparser_for(c, method, sub)
				cls.COMMANDS[command][c] = method

	@classmethod
	def get_commands(cls, prefix="", delim="_"):
		"""
		Iterator yielding object methods with

		:prefix: filter object methods to return
		"""
		parent_members = [k for k, v in getmembers(Command)]
		for method, func in getmembers(cls):
			if callable(func) and method not in parent_members and method.startswith(prefix):
					command = findall("{pf}{delim}?(.*)".format(pf=prefix, delim=delim), method)[0]
					yield (command, method)

	@classmethod
	def set_subparser_for(cls, command, method, subparser):
		"""
		Takes a subparser as argument and add arguments corresponding to command in it.

		:command: name to display in the help
		:method: function name corresponding to the command
		:subparser: subparser object to add argument(s) to
		"""

		def add_pos_argument(sub, label, arg):
			if arg["type"] == bool:
				raise CommandTypeError("bool type not supported as positional argument")
			if "value" in arg:
				if arg["type"] in [str, int, float]:
					sub.add_argument(label, nargs='?', default=arg["value"], type=arg["type"], help=arg["help_line"])
			elif "values" in arg:
				if arg["type"] in [str, int, float]:
					sub.add_argument(label, nargs='?', default=arg["values"][0], choices=arg["values"], type=arg["type"], help=arg["help_line"])
				elif arg["type"] == list:
					sub.add_argument(label, nargs='+', default=arg["values"][0], choices=arg["values"], help=arg["help_line"])
			else:
				sub.add_argument(label, type=arg["type"], help=arg["help_line"])

		def add_opt_argument(sub, label, arg, add_alias=True):
			if arg["type"] == bool:
				if add_alias:
					sub.add_argument(arg["alias"], arg["name"], action="store_true", default=False, help=arg["help_line"])
				else:
					sub.add_argument(arg["name"], action="store_true", default=False, help=arg["help_line"])

			elif arg["type"] in [str, int, float] and "value" in arg:
				if add_alias:
					sub.add_argument(arg["alias"], arg["name"], type=arg["type"], default=arg["value"], help=arg["help_line"])
				else:
					sub.add_argument(arg["name"], type=arg["type"], default=arg["value"], help=arg["help_line"])
			elif arg["type"] == list and "values" not in arg:
				sub.add_argument(label, nargs="*", help=arg["help_line"])
			elif "values" in arg:
				if arg["type"] == list:
					sub.add_argument(label, choices=arg["values"], default=arg["values"][0], nargs="*", help=arg["help_line"])
				else:
					sub.add_argument(label, type=arg["type"], choices=arg["values"], default=arg["values"][0], nargs="?", help=arg["help_line"])
			else:
				if add_alias:
					sub.add_argument(arg["alias"], arg["name"], type=arg["type"], help=arg["help_line"])
				else:
					sub.add_argument(arg["name"], type=arg["type"], help=arg["help_line"])
		
		func = getattr(cls, method)

		args_info = cls.__parse_docstring(func.__doc__)
		if args_info == {}:
			return

		c = subparser.add_parser(command, help=args_info["help_line"])

		if "arguments" in args_info:
			for label, arg in args_info["arguments"].items():
				if arg["pos"]:
					add_pos_argument(c, label, arg)
				else:
					try:
						add_opt_argument(c, label, arg, add_alias=True)
					except ArgumentError as e:
						add_opt_argument(c, label, arg, add_alias=False)

	def has_option(self, method, option):
		"""
		Returns `true` if a given method has a certain option.

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
		Returns the default value(s) of a certain argument/option of a given method.

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

	def dispatch_command(self, args):
		"""
		Executes the corresponding command with provided args.
		Returns None if no command is provided otherwise forwards the command return.
		Raises CommandNotFoundError if the command is not registered, should not happen.

		:args: result from ArgumentParser.parse_args()
		"""
		arguments = {k: v for k, v in vars(args).items() if v is not None}
		for c in self.COMMANDS.keys():
			cmd = arguments.get(c, False)
			idx = c
			if cmd:
				break
		else:
			return None

		if cmd not in self.COMMANDS[idx]:
			raise CommandNotFoundError("{cmd} not registered".format(cmd=cmd))

		return getattr(self, self.COMMANDS[idx][cmd])(arguments)
