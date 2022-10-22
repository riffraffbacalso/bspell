from argparse import ArgumentParser, Namespace
from formatting import fprint
from scrape import get_letters
from solve import solve_bee
from word_freq import sort_by_freq


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-w",
        "--word-src",
        default="OPTED",
        metavar="<word source>",
        help="the source of words used for puzzle solutions",
    )
    return parser.parse_args()


def main() -> None:
    args = get_args()
    words = solve_bee(get_letters(), args.word_src)
    words = sort_by_freq(words)
    fprint(words)


if __name__ == "__main__":
    main()
