# Flagparse

[![Build Status][BuildStatus]](https://travis-ci.org/ybubnov/flagparse)


Flagparse is a library for building modular command-line interfaces with
accent on nested commands. This library removes the pain of manually
constructing the argument parsing and applying handler for each command, all
of this is done by this tiny library.

## Installation

```bash
pip install flagparse
```

## Usage and documentation

Please see the [wiki][Wiki] for basic usage and other documentation of using
flagparse.

Here is an example of a simple Flagparse app:
```py
import flagparse


class Sum(flagparse.SubCommand):
    """Sub-command to handle numbers summation."""

    name = "sum"
    arguments = [
        (["integers"],
         dict(metavar="INT",
              type=int,
              nargs="+",
              help="integers to be summed")),
    ]

    def handle(self, args: flagparse.Namespace) -> None:
        print(sum(args.integers))


class Calc(flagparse.Command):
    """A simple calculator that sums numbers."""

    name = "calc"


if __name__ == "__main__":
    Calc(subcommands=[Sum]).parse()
```

How it looks when run:
```bash
$ python main.py sum 1 2 3
6
```

## License

The openflow library is distributed under MIT license, therefore you are free
to do with code whatever you want. See the [LICENSE](LICENSE) file for full
license text.

[BuildStatus]: https://travis-ci.org/ybubnov/flagparse.svg?branch=master
[Wiki]: https://github.com/ybubnov/flagparse/wiki
