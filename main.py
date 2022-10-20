import textwrap as tw
from highlight import highlight_lines
from scrape import get_letters
from solve import solve_bee
from word_freq import sort_by_freq


def main() -> None:
    words = solve_bee(get_letters())
    words = sort_by_freq(words)
    words = tw.wrap(text=" ".join(words))
    words = highlight_lines(words)
    print(*(f"  {line}" for line in words), sep="\n")


if __name__ == "__main__":
    main()
