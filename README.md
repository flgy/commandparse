# commandparse

Module to parse command based CLI application.

Usage:

* Subclass the Command class
* Add a method with a name such as `prefix_commandname` with kwargs as required argument
* Create an ArgumentParser instance
* Call the `Subclass.add_suparsers` with the ArgumentParser instance and other settings
* Use the `dispatch_command` function with the args returned by `parser.parse_args()`

```
parser = ArgumentParser(...)
[...]
Subclass.add_subparsers(parser, prefixes=["get_", "do_", ...], title="commands", description="available commands")

cmd = Subclass(...)
cmd.dispatch_command(commands, args)
```

See example.py for a more complete example. For a real world application using this lib, see: https://github.com/franc-pentest/ldeep
