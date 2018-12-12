# commandparse

Module to parse command based CLI application.

Usage:

* Subclass the Command class
* Add a method with a name such as `prefix_commandname` with kwargs as required argument
* Create a an ArgumentParser and declare a subparser per command
* Register the commands in a dictionary
* Use the `dispatch_command` function with the commands and args returned by `parser.parse_args()`

```
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
```

See example.py for a more complete example. For a real world application using this lib, see: https://github.com/franc-pentest/ldeep
