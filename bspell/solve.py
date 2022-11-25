import re

from words import Words


def solve_bee(problem: str, word_src: str) -> list[str]:
    return [
        word
        for word in Words.get_words(word_src)
        if re.match(rf"[{problem}]{{4,}}\Z", word) and problem[0] in word
    ]


if __name__ == "__main__":
    print(solve_bee("problem", "OS"))
