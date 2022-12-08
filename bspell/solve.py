import re

from words import Words


def solve_bee(problem: str, word_src: str) -> list[str]:
    reg = re.compile(rf"[{problem}]{{4,}}\Z")
    return [
        word
        for word in Words.get_words(word_src)
        if reg.match(word) and problem[0] in word
    ]
