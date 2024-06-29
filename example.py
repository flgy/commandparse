#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argparse import ArgumentParser
from commandparse import Command
from argcomplete import autocomplete


class Example(Command):
    # Can have arbitrary arguments
    def __init__(self):
        pass

    # Will autocomplete based on the iterable contained in the lookup
    def _autocomplete(selector):
        lookup = {"metrics": ["a", "b", "c"]}
        return lambda **x: lookup.get(selector, "None")

    def get_info(self, kwargs):
        """
        Return infos.

        Arguments:
            #arg:string:metrics
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
    Example.add_subparsers(
        parser, prefixes=["get_"], title="commands", description="available commands"
    )
    autocomplete(parser)
    args = parser.parse_args()

    example = Example()
    example.dispatch_command(args)
