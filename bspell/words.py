from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from itertools import chain
from string import ascii_lowercase
from typing import Iterator
from unidecode import unidecode
from retry_msg import retry_msg
import os
import re
import tarfile
import httpx

OS_WORDS_PATH = "/usr/share/dict/words"
ALT_WORDS_PATH = "bspell/words"
ALT_WORD_SRCS = ["OPTED", "chirico"]
OPTED_URL = "https://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"
CHIRICO_URL = "https://sourceforge.net/projects/souptonuts/files/souptonuts/dictionary/linuxwords.1.tar.gz/download"
TAR_MEMBERS = [
    "linuxwords.1/linux.words",
    "linuxwords.1/linux.words.backup.fedora.standard",
]
OPTED_REG = r"(?<=<B>)[A-Z][a-zA-Z]{3,}(?=</B>)"
VALID_REG = r"[^']{4,}\Z"


class Words:
    @staticmethod
    def read_OS_words() -> list[str]:
        with open(OS_WORDS_PATH) as f:
            return [word.lower() for word in f.read().split("\n") if len(word) >= 4]

    @staticmethod
    def request_OPTED_words() -> list[str]:
        with httpx.Client(http2=True) as client:

            def extract_list(line_gen: Iterator[str]) -> list[str]:
                word_gen = (
                    match.group().lower()
                    for line in line_gen
                    if (match := re.search(OPTED_REG, line))
                )
                return list(dict.fromkeys(word_gen))

            @retry_msg("persistent network error when retrieving OPTED words")
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

    @staticmethod
    def request_chirico_words() -> list[str]:
        @retry_msg("persistent network error when retrieving chirico words")
        def request_redirect() -> httpx.Response:
            return httpx.get(CHIRICO_URL, follow_redirects=True)

        res = request_redirect()
        data = BytesIO(res.read())

        with tarfile.open(fileobj=data) as tf:
            big_reader = tf.extractfile(TAR_MEMBERS[0])
            fed_reader = tf.extractfile(TAR_MEMBERS[1])
            assert big_reader and fed_reader
            big_gen = (word for word in big_reader.read().split(b"\n"))
            fed_gen = (word for word in fed_reader.read().split(b"\n"))
            word_gen = (word.decode("latin1") for word in chain(big_gen, fed_gen))
            utf_gen = (unidecode(word) for word in word_gen)
            lower_gen = (word.lower() for word in utf_gen)
            valid_gen = (word for word in lower_gen if re.match(VALID_REG, word))
            words = sorted(list(dict.fromkeys(valid_gen)))

        with open(f"{ALT_WORDS_PATH}/chirico.words", "w") as f:
            print(*words, file=f, sep="\n")

        return words

    @staticmethod
    def get_words(word_src: str) -> list[str]:
        if word_src == "OS":
            return Words.read_OS_words()
        elif word_src in ALT_WORD_SRCS:
            if not os.path.exists(ALT_WORDS_PATH):
                os.mkdir(ALT_WORDS_PATH)
            if f"{word_src}.words" not in os.listdir(ALT_WORDS_PATH):
                print(f"  retrieving {word_src} words...")
                return getattr(Words, f"request_{word_src}_words")()
            else:
                with open(f"{ALT_WORDS_PATH}/{word_src}.words") as f:
                    return f.read().strip("\n").split("\n")
        else:
            raise ValueError(f"invalid word source: '{word_src}'")


if __name__ == "__main__":
    print(Words.get_words("OPTED"))
