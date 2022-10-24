from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from string import ascii_lowercase
from typing import Iterator
import os
import re
import httpx
import nltk

OS_DICT_PATH = "/usr/share/dict/words"
OPTED_PATH = "bspell/words"
URL = "https://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"
REGEX = r"(?<=<B>)[A-Z][a-zA-Z]{3,}(?=</B>)"
MISSING_WORDS = ["near", "behaviour", "harbour", "humour", "box", "colour"]


def read_OS_words() -> list[str]:
    with open("/usr/share/dict/words") as f:
        return [word for word in f.read().split("\n") if len(word) >= 4]


def request_OPTED_words() -> None:
    with httpx.Client(http2=True) as client:

        def write_out(line_gen: Iterator[str], letter: str) -> None:
            with open(f"{OPTED_PATH}/{letter}.words", "w") as f:
                word_gen = (
                    match.group().lower()
                    for line in line_gen
                    if (match := re.search(REGEX, line))
                )
                print(
                    *list(dict.fromkeys(word_gen)),
                    file=f,
                    sep=",",
                )

        def request_write(letter: str) -> None:
            with client.stream("GET", f"{URL}{letter}.html") as res:
                line_gen = res.iter_lines()
                while next(line_gen) != "<BODY>\n":
                    pass
                write_out(line_gen, letter)

        with ThreadPoolExecutor(max_workers=26) as pool:
            pool.map(request_write, ascii_lowercase)


def read_OPTED_words() -> list[str]:
    words = []
    if not os.path.exists(OPTED_PATH):
        os.mkdir(OPTED_PATH)
    if not set(os.listdir(OPTED_PATH)) >= {
        f"{letter}.words" for letter in ascii_lowercase
    }:
        print("  retrieving OPTED words...")
        request_OPTED_words()
    with ExitStack() as stack:
        files = [
            stack.enter_context(open(f"{OPTED_PATH}/{letter}.words"))
            for letter in ascii_lowercase
        ]
        words = sum([f.strip("\n").split(",") for f in next(zip(*files))], [])
    return words


def read_NLTK_words():
    nltk.download("words", quiet=True)
    from nltk.corpus import words  # fmt:skip
    return words.words("en") + MISSING_WORDS


def get_words(word_src: str) -> list[str]:
    if word_src == "OS":
        word_list = read_OS_words()
    elif word_src == "OPTED":
        word_list = read_OPTED_words()
    elif word_src == "NLTK":
        word_list = read_NLTK_words()
    else:
        raise ValueError(f"invalid word source: '{word_src}'")
    return word_list


if __name__ == "__main__":
    print(get_words("OPTED"))
