import textwrap as tw
from scrape import get_letters
from solve import solve_bee
from word_freq import sort_words


def main() -> None:
    words = solve_bee(get_letters())
    words = sort_words(words)
    words = tw.wrap(text=" ".join(words))
    print(*words, sep="\n")


if __name__ == "__main__":
    main()
