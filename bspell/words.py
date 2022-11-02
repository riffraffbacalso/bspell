from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from string import ascii_lowercase
from typing import Iterator
import gzip
import os
import re
import httpx

OS_WORDS_PATH = "/usr/share/dict/words"
ALT_WORDS_PATH = "bspell/words"
OPTED_URL = "https://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"
CHIRICO_URL = "https://sourceforge.net/projects/souptonuts/files/souptonuts/dictionary/linuxwords.1.tar.gz/download"
OPTED_REGEX = r"(?<=<B>)[A-Z][a-zA-Z]{3,}(?=</B>)"
CHIRICO_REGEX = r"[^']{4,}\Z"


def read_OS_words() -> list[str]:
    with open(OS_WORDS_PATH) as f:
        return [word.lower() for word in f.read().split("\n") if len(word) >= 4]


def request_OPTED_words() -> list[str]:
    with httpx.Client(http2=True) as client:

        def extract_list(line_gen: Iterator[str]) -> list[str]:
            word_gen = (
                match.group().lower()
                for line in line_gen
                if (match := re.search(OPTED_REGEX, line))
            )
            return list(dict.fromkeys(word_gen))

        def request_for_letter(letter: str) -> list[str]:
            with client.stream("GET", f"{OPTED_URL}{letter}.html") as res:
                line_gen = res.iter_lines()
                while next(line_gen) != "<BODY>\n":
                    pass
                return extract_list(line_gen)

        with ThreadPoolExecutor(max_workers=26) as pool:
            words = sum(pool.map(request_for_letter, ascii_lowercase), [])

    with open(f"{ALT_WORDS_PATH}/OPTED.words", "w") as f:
        print(*words, file=f, sep="\n")
    
    return words


def read_OPTED_words() -> list[str]:
    if not os.path.exists(ALT_WORDS_PATH):
        os.mkdir(ALT_WORDS_PATH)
    if "OPTED.words" not in os.listdir(ALT_WORDS_PATH):
        print("  retrieving OPTED words...")
        return request_OPTED_words()
    else:
        with open(f"{ALT_WORDS_PATH}/OPTED.words") as f:
            return f.read().strip("\n").split("\n")


def request_chirico_words() -> list[str]:
    res = httpx.get(CHIRICO_URL, follow_redirects=True)
    data = gzip.decompress(res.content)
    byte_gen = (char.to_bytes(1, "big") for char in data)
    count = 0
    while count < 7:
        while (byte := next(byte_gen)) != b"c":
            pass
        if list(islice(byte_gen, 6)) == [b"h", b"i", b"r", b"i", b"c", b"o"]:
            count += 1
            for _ in range(6):
                next(byte_gen)
    while (byte := next(byte_gen)) == b"\x00":
        pass
    next(byte_gen)
    words = "".join(
        str(byte).lower()[2:-1] for byte in byte_gen if byte != b"\x00"
    ).split(r"\n")
    words = [word for word in dict.fromkeys(words) if re.match(CHIRICO_REGEX, word)]
    with open(f"{ALT_WORDS_PATH}/chirico.words", "w") as f:
        print(*words, file=f, sep="\n")
    return words


def read_chirico_words() -> list[str]:
    if not os.path.exists(ALT_WORDS_PATH):
        os.mkdir(ALT_WORDS_PATH)
    if "chirico.words" not in os.listdir(ALT_WORDS_PATH):
        print("  retrieving chirico words...")
        return request_chirico_words()
    else:
        with open(f"{ALT_WORDS_PATH}/chirico.words") as f:
            return [word for word in f.read().strip("\n").split("\n")]


def get_words(word_src: str) -> list[str]:
    if word_src == "OS":
        return read_OS_words()
    elif word_src == "OPTED":
        return read_OPTED_words()
    elif word_src == "chirico":
        return read_chirico_words()
    else:
        raise ValueError(f"invalid word source: '{word_src}'")


if __name__ == "__main__":
    print(get_words("OPTED"))
