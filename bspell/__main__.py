from argparse import ArgumentParser, Namespace

from formatting import fprint
from scrape import get_problem
from solve import solve_bee
from word_freq import sort_by_freq


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "problem",
        nargs="?",
        default=None,
        metavar="<problem>",
        help="problem string manual input"
    )
    parser.add_argument(
        "-w",
        "--word-src",
        default="OS",
        metavar="<word source>",
        help="the source of words used for puzzle solutions",
    )
    return parser.parse_args()


def main() -> None:
    args = get_args()
    problem = args.problem if args.problem else get_problem()
    words = solve_bee(problem, args.word_src)
    words = sort_by_freq(words)
    fprint(words)


if __name__ == "__main__":
    main()
