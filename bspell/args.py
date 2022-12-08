from argparse import Action, ArgumentError, ArgumentParser, Namespace
import re

PROBLEM_REG = re.compile(r"^(?!.*(.).*\1)[a-z]{7}\Z")


class ValidateAction(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: str | None,
        option_string: str | None = None,
    ) -> None:
        del parser, option_string
        if value and not PROBLEM_REG.match(value):
            raise ArgumentError(
                None,
                f"argument <problem>: invalid puzzle: '{value}' (must be seven unique alphabet characters)",
            )
        setattr(namespace, self.dest, value)


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "problem",
        nargs="?",
        action=ValidateAction,
        default=None,
        metavar="<problem>",
        help="problem string manual input",
    )
    parser.add_argument(
        "-w",
        "--word-src",
        choices=["OPTED", "chirico"],
        default="OS",
        metavar="<word source>",
        help="the source of words used for puzzle solutions",
    )
    return parser.parse_args()
