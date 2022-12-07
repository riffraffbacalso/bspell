import textwrap as tw

HIL = "\033[1;38;5;2m"
RST = "\033[0m"


def wrap(words: list[str]) -> list[str]:
    return tw.wrap(" ".join(words))


def highlight_lines(lines: list[str]) -> list[str]:
    def highlight(line: str) -> str:
        return " ".join(
            (
                f"{HIL}{word}{RST}" if len(set(word)) == 7 else word
                for word in line.split()
            )
        )

    return [highlight(line) for line in lines]


def fprint(words: list[str]) -> None:
    words = highlight_lines(wrap(words))
    print(*(f"  {line}" for line in words), sep="\n")
