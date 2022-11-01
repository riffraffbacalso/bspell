from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from string import ascii_lowercase
from typing import Iterator
import gzip
import os
import re
import httpx

OS_DICT_PATH = "/usr/share/dict/words"
ALT_PATH = "bspell/words"
OPTED_URL = "https://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"
CHIRICO_URL = "https://sourceforge.net/projects/souptonuts/files/souptonuts/dictionary/linuxwords.1.tar.gz/download"
OPTED_REGEX = r"(?<=<B>)[A-Z][a-zA-Z]{3,}(?=</B>)"
CHIRICO_REGEX = r"[^']{4,}\Z"


def read_OS_words() -> list[str]:
    with open(OS_DICT_PATH) as f:
        return [word.lower() for word in f.read().split("\n") if len(word) >= 4]


def request_OPTED_words() -> list[str]:
    with httpx.Client(http2=True) as client:

        def extract_list(line_gen: Iterator[str], letter: str) -> list[str]:
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
                return extract_list(line_gen, letter)

        with ThreadPoolExecutor(max_workers=26) as pool:
            word_list = sum(pool.map(request_for_letter, ascii_lowercase), [])
        with open(f"{ALT_PATH}/OPTED.words", "w") as f:
            print(*word_list, file=f, sep="\n")
        return word_list


def read_OPTED_words() -> list[str]:
    words = []
    if not os.path.exists(ALT_PATH):
        os.mkdir(ALT_PATH)
    if not set(os.listdir(ALT_PATH)) >= {
        f"{letter}.words" for letter in ascii_lowercase
    }:
        print("  retrieving OPTED words...")
        words = request_OPTED_words()
    else:
        with open(f"{ALT_PATH}/OPTED.words") as f:
            words = f.read().strip("\n").split("\n")
    return words


def request_chirico_words() -> None:
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
    with open(f"{ALT_PATH}/chirico.words", "wb") as f:
        while (byte := next(byte_gen)) != b"\x00":
            f.write(byte)


def read_chirico_words() -> list[str]:
    words = []
    if not os.path.exists(ALT_PATH):
        os.mkdir(ALT_PATH)
    if "chirico.words" not in os.listdir(ALT_PATH):
        print("  retrieving chirico words...")
        request_chirico_words()
    with open(f"{ALT_PATH}/chirico.words", "rb") as f:
        words = [
            word.lower()
            for b_word in f.read().strip(b"\n").split(b"\n")
            if re.match(CHIRICO_REGEX, (word := str(b_word)[2:-1]))
        ]
    return words


def get_words(word_src: str) -> list[str]:
    if word_src == "OS":
        word_list = read_OS_words()
    elif word_src == "OPTED":
        word_list = read_OPTED_words()
    elif word_src == "chirico":
        word_list = read_chirico_words()
    else:
        raise ValueError(f"invalid word source: '{word_src}'")
    return word_list


if __name__ == "__main__":
    print(get_words("OPTED"))
