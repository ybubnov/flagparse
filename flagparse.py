"""Command-line parsing library

This module is an extension of argparse parsing library that utilizes a
class-oriented approach of declaring command-line interfaces.

The following is a simple usage example that sums integers from the
command-line and prints the result.

    class Sum(flagparse.Command):

        name = "sum"
        description = "sum the integers at the command line"

        arguments = [
            (["integers"],
             dict(metavar="INT",
                  type=int,
                  nargs="+",
                  help="integers to be summed")),
        ]

        def handle(self, args: flagparse.Namespace) -> None:
            if len(args.integers) < 2:
                raise flagparse.ExitError("at least 2 integers expected")
            print(sum(args.integers))

    Sum().parse()


The module contains the following public classes:

    - Command -- The main entry point for parsing arguments of the program. It
                 can specify either a self-sufficient command or define a
                 hierarchy of sub-commands.

    - SubCommand -- The sub-command for building complex nested command-line
                    interfaces.

    - ExitError -- The exception to specify what error should be returned
                   by the program. It is a placeholder for exit code and
                   optional message that will be shown before the exit.
"""

__version__ = "0.0.2"


import argparse
import io
import sys

from typing import Any, Sequence, Optional, Union


class Namespace(argparse.Namespace):
    """Namespace to hold parsed options as object attributes."""
    pass


class ExitError(Exception):
    """Exception used to specify flag handling error.

    Attributes:
        code -- process exit code
        message -- optional message printed before exit
    """

    def __init__(self, code: int = 1, message: str = ""):
        self.code = code
        self.message = message

        super().__init__(f"{self.code}, message={self.message}")


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


class _Attr:

    def __init__(self, name: str, required: Union[bool] = False):
        self.name = name
        self.required = bool(required)


class _Meta(Namespace):
    """Holds meta information about command or sub-command."""

    def __init__(self, obj: Any, attributes: Sequence[_Attr]):
        attrs = {}
        for attr in attributes:
            attr_val = getattr(obj, attr.name, None)
            if attr.required and attr_val is None:
                raise ValueError(f"required attribute {attr.name} is missing")
            attrs[attr.name] = attr_val
        super().__init__(**attrs)


class SubCommand:
    """Parser for sub-commands of the parent command.

    Attributes:
        subparsers -- a list of argument sub-parsers
    """

    __attributes__ = [
        _Attr("name", required=True),
        _Attr("aliases"),
        _Attr("arguments"),
        _Attr("help"),
        _Attr("description"),
        _Attr("subcommands"),
    ]

    def __init__(self, subparsers):
        # Copy all meta parameters of the command into the __meta__
        # dictionary, so it can be accessible during the setup of commands.
        self.__meta__ = _Meta(self, self.__attributes__)
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
            self.subcommands = [c(subparsers) for c in
                                self.__meta__.subcommands]

    def handle(self, args: Namespace):
        self.subparser.print_help()


class Command:
    """Parser for parsing command line strings and handling commands.

    Arguments:
        subcommands -- optional list of sub-commands
    """

    __attributes__ = [
        _Attr("name", required=True),
        _Attr("arguments"),
        _Attr("description"),
    ]

    def __init__(self,
                 subcommands: Optional[Sequence[SubCommand]] = None):
        self.__meta__ = _Meta(self, self.__attributes__)

        self.parser = argparse.ArgumentParser(
            formatter_class=_Formatter,
            prog=self.__meta__.name,
            description=self.__meta__.description,
        )

        self.parser.set_defaults(func=self.handle)

        for args, kwargs in self.__meta__.arguments or []:
            self.parser.add_argument(*args, **kwargs)

        if subcommands:
            subparsers = self.parser.add_subparsers()
            self.subcommands = [c(subparsers) for c in subcommands]

    def handle(self, args: Namespace) -> None:
        self.parser.print_help()

    def parse(self,
              args: Optional[Sequence[str]] = None,
              errlog: io.TextIOBase = sys.stderr):
        try:
            args = self.parser.parse_args(args)
            return args.func(args=Namespace(**args.__dict__))
        except ExitError as e:
            if e.message:
                errlog.write(f"{e.message}\n")
                errlog.flush()
            sys.exit(e.code)
        except Exception as e:
            errlog.write(f"{e}\n")
            errlog.flush()
            sys.exit(1)
        finally:
            sys.exit(0)
