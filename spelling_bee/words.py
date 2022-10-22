from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
import re
from string import ascii_lowercase
from typing import Iterator
import httpx
import nltk


PATH = "spelling_bee/words"
URL = "https://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"
REGEX = r"(?<=<B>)[A-Z][a-zA-Z]*(?=</B>)"
MISSING_WORDS = ["near", "behaviour", "harbour", "humour", "box", "colour"]


def request_OPTED_words() -> None:
    with httpx.Client(http2=True) as client:

        def write_out(gen: Iterator[str], letter: str) -> None:
            with open(f"{PATH}/{letter}.words", "w") as f:
                word_gen = (
                    word.lower()
                    for line in gen
                    if (match := re.search(REGEX, line))
                    and len(word := match.group()) >= 4
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
    with ExitStack() as stack:
        files = [
            stack.enter_context(open(f"{PATH}/{letter}.words"))
            for letter in ascii_lowercase
        ]
        words = sum([f.strip("\n").split(",") for f in next(zip(*files))], [])
    return words


def read_NLTK_words():
    nltk.download("words", quiet=True)
    from nltk.corpus import words

    return words.words("en") + MISSING_WORDS


def get_words(word_src: str) -> list[str]:
    if word_src == "OPTED":
        word_list = read_OPTED_words()
    elif word_src == "NLTK":
        word_list = read_NLTK_words()
    else:
        raise ValueError(f"invalid word_src: '{word_src}'")
    return word_list


if __name__ == "__main__":
    print(get_words("OPTED"))
