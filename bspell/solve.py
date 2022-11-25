import re

from words import Words

PROBLEM_REG = r"^(?!.*(.).*\1)[a-z]{7}\Z"


def solve_bee(problem: str, word_src: str) -> list[str]:
    if not re.match(PROBLEM_REG, problem):
        raise ValueError(
            f'puzzle must be seven unique alphabet characters, not "{problem}"'
        )
    return [
        word
        for word in Words.get_words(word_src)
        if re.match(rf"[{problem}]{{4,}}\Z", word) and problem[0] in word
    ]


if __name__ == "__main__":
    print(solve_bee("problem", "OS"))
