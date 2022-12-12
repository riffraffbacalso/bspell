from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from itertools import chain
from string import ascii_lowercase
from typing import Iterator, TextIO
import fileinput
import os
import re
import tarfile

from retry_msg import retry_msg

from unidecode import unidecode
import httpx

OS_WORDS_PATH = "/usr/share/dict/words"
ALT_WORDS_PATH = "bspell/words"
OPTED_URL = "https://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"
CHIRICO_URL = "https://sourceforge.net/projects/souptonuts/files/souptonuts/dictionary/linuxwords.1.tar.gz/download"
TAR_MEMBERS = [
    "linuxwords.1/linux.words",
    "linuxwords.1/linux.words.backup.fedora.standard",
]
OPTED_REG = re.compile(r"(?<=<B>)[A-Z][a-zA-Z]{3,}(?=</B>)")
VALID_REG = re.compile(r"[^']{4,}\Z")


class Words:
    @staticmethod
    def request_OPTED_words() -> Iterator[str]:
        with httpx.Client(http2=True) as client:

            @retry_msg("persistent network error when retrieving OPTED words")
            def request_for_letter(letter: str) -> Iterator[str]:
                with client.stream("GET", f"{OPTED_URL}{letter}.html") as res:
                    line_gen = res.iter_lines()
                    while next(line_gen) != "<BODY>\n":
                        pass
                    word_gen = (
                        match.group().lower()
                        for line in line_gen
                        if (match := OPTED_REG.search(line))
                    )
                    return (word for word in dict.fromkeys(word_gen))

            with ThreadPoolExecutor(max_workers=26) as pool:
                return chain(*pool.map(request_for_letter, ascii_lowercase))

    @staticmethod
    def request_chirico_words() -> Iterator[str]:
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
            valid_gen = (word for word in lower_gen if VALID_REG.match(word))
            return (word for word in dict.fromkeys(valid_gen))

    @staticmethod
    def print_gen(gen: Iterator[str], file: TextIO) -> Iterator[str]:
        while True:
            try:
                word = next(gen)
                file.write(f"{word}\n")
                yield word
            except StopIteration:
                file.close()
                break

    @staticmethod
    def get_words(word_src: str) -> Iterator[str]:
        if word_src == "OS":
            lower_gen = (
                word.lower()
                for line in open(OS_WORDS_PATH)
                if len(word := line.strip()) >= 4
            )
            return (word for word in dict.fromkeys(lower_gen))
        else:
            if not os.path.exists(ALT_WORDS_PATH):
                os.mkdir(ALT_WORDS_PATH)
            if f"{word_src}.words" not in os.listdir(ALT_WORDS_PATH):
                f = open(f"{ALT_WORDS_PATH}/{word_src}.words", "w")
                print(f"  retrieving {word_src} words...")
                word_gen = getattr(Words, f"request_{word_src}_words")()
                return Words.print_gen(word_gen, f)
            else:
                return (
                    line.strip()
                    for line in fileinput.input(f"{ALT_WORDS_PATH}/{word_src}.words")
                )
