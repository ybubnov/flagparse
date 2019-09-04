import io
import random
import unittest
import unittest.mock

import flagparse


class Sum(flagparse.SubCommand):
    """Test implementation of sub sub-command."""

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
    """Main entry command of test calculation program."""

    name = "calc"


class TestFlagParse(unittest.TestCase):

    @unittest.mock.patch("sys.exit")
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_calc(self, stdout_mock, exit_mock) -> None:
        nums = [random.randint(0, 100)] * 10

        s = Calc(subcommands=[Sum])
        s.parse(["sum"] + list(map(str, nums)))

        self.assertEqual(f"{sum(nums)}\n", stdout_mock.getvalue())
        exit_mock.assert_called_with(0)


if __name__ == "__main__":
    unittest.main()
