import re
from words import get_words


def solve_bee(letters: str, word_src: str) -> list[str]:
    return [
        word
        for word in get_words(word_src)
        if re.match(rf"[{letters}]{{4,}}\Z", word) and letters[0] in word
    ]


if __name__ == "__main__":
    print(solve_bee("problem", "OPTED"))
