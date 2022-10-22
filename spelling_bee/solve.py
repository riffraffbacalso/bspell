import re
from words import get_words


def solve_bee(letters: str, word_src: str) -> list[str]:
    words = get_words(word_src)
    return [
        word
        for word in words
        if bool(re.match(rf"[{letters}]+\Z", word))
        and len(word) >= 4
        and letters[0] in word
    ]


if __name__ == "__main__":
    print(solve_bee("problem", "OPTED"))
