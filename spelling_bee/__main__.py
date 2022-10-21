from formatting import fprint
from scrape import get_letters
from solve import solve_bee
from word_freq import sort_by_freq


def main() -> None:
    words = solve_bee(get_letters())
    words = sort_by_freq(words)
    fprint(words)


if __name__ == "__main__":
    main()
