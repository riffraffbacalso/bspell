HIL = "\033[1;38;5;2m"
RST = "\033[0m"


def highlight(line: str) -> str:
    return " ".join(
        (f"{HIL}{word}{RST}" if len(set(word)) == 7 else word for word in line.split())
    )


def highlight_lines(lines: list[str]) -> list[str]:
    return [highlight(line) for line in lines]


if __name__ == "__main__":
    print(
        *highlight_lines(["abcdefg abcdef aabcdef", "abcdef aabcdef abcdefg"]),
        sep="\n",
    )
