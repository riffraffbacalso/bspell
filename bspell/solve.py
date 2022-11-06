import re
from words import Words

LETTER_REG = r"[a-z]{7}\Z"


def solve_bee(letters: str, word_src: str) -> list[str]:
    if not re.match(LETTER_REG, letters):
        raise ValueError(f'puzzle must be seven alphabet characters, not "{letters}"')
    return [
        word
        for word in Words.get_words(word_src)
        if re.match(rf"[{letters}]{{4,}}\Z", word) and letters[0] in word
    ]


if __name__ == "__main__":
    print(solve_bee("problem", "OS"))
