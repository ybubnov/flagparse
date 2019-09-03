"""Command-line parsing library

This module is an extension of argparse parsing library that utilizes a
class-oriented approach of declaring command-line interfaces.

The following is a simple usage example that sums integers from the
command-line and prints the result.

    class Sum(flagparse.Command):

        help = "specify integers to get the sum"
        description = "sum the integers at the command line"

        arguments = [
            (["integers"],
             dict(metavar="INT",
                  type=int,
                  nargs="+",
                  help="integers to be summed")),
        ]

        def handle(self, args):
            print(sum(args.integers))
            return flagparse.ExitStatus.Success

    sys.exit(Sum("sum").parse().value)
"""

__version__ = "0.0.1"


import argparse
import enum

from typing import Sequence, Optional


class Namespace(argparse.Namespace):
    """Namespace to hold parsed options as object attributes."""
    pass


class ExitStatus(enum.Enum):
    Success = 0
    Failure = 1


class _Formatter(argparse.ArgumentDefaultsHelpFormatter):
    """Formatter to format arguments with default values for wide screens.

    Print the usage of commands to 140 character-wide terminals.
    """

    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=48,
                 width=140):
        super().__init__(prog, indent_increment, max_help_position, width)


class SubCommand:
    """Parser for sub-commands of the parent command."""

    __attributes__ = [
        "name",
        "aliases",
        "arguments",
        "help",
        "description",
        "subcommands",
    ]

    def __init__(self, subparsers):
        # Copy all meta parameters of the command into the __meta__ dictionary,
        # so it can be accessible during the setup of commands.
        attrs = {attr: getattr(self, attr, None)
                 for attr in self.__attributes__}

        self.__meta__ = Namespace(**attrs)
        self.subcommands = []

        self.subparser = subparsers.add_parser(
            name=self.__meta__.name,
            help=self.__meta__.help,
            aliases=(self.__meta__.aliases or []),
            description=self.__meta__.description,
            formatter_class=_Formatter)

        for args, kwargs in self.__meta__.arguments or []:
            self.subparser.add_argument(*args, **kwargs)

        # At least print the help message for the command.
        self.subparser.set_defaults(func=self.handle)

        if self.__meta__.subcommands:
            subparsers = self.subparser.add_subparsers(dest=self.__meta__.name)
            self.subcommands = [c(subparsers) for c in self.__meta__.subcommands]

    def handle(self, args: Namespace) -> ExitStatus:
        self.subparser.print_help()
        return ExitStatus.Success


class Command:
    """Parser for parsing command line strings and handling commands.

    Arguments:
        name -- name of the command
        subcommands -- optional list of sub-commands
    """

    def __init__(self, name: str, subcommands: Optional[SubCommand] = None):
        self.parser = argparse.ArgumentParser(
            prog=name, formatter_class=_Formatter)

        self.parser.set_defaults(func=self.handle)

        for args, kwargs in self.arguments:
            self.parser.add_argument(*args, **kwargs)

        if subcommands:
            subparsers = self.parser.add_subparsers()
            self.subcommands = [c(subparsers) for c in subcommands]

    def handle(self, args: Namespace) -> ExitStatus:
        self.parser.print_help()
        return ExitStatus.Failure

    def parse(self):
        args = self.parser.parse_args()
        return args.func(args=Namespace(**args.__dict__))
