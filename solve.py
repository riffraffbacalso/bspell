import re
import nltk

nltk.download("words", quiet=True)

from nltk.corpus import words


def solve_bee(letters: str) -> list[str]:
    return [
        word
        for word in words.words()
        if bool(re.match(rf"[{letters}]+\Z", word))
        and len(word) >= 4
        and letters[0] in word
    ]


if __name__ == "__main__":
    print(solve_bee("problem"))
