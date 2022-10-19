import textwrap as tw
from scrape import get_letters
from solve import solve_bee


def main() -> None:
    solutions = solve_bee(get_letters())
    words = tw.wrap(text=" ".join(solutions))
    print(*words, sep="\n")


if __name__ == "__main__":
    main()
