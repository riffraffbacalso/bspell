import re
import nltk

nltk.download("words")

from nltk.corpus import words

if __name__ == "__main__":
    answers = [
        word
        for word in words.words()
        if bool(re.match(r"[mntyiac]+\Z", word)) and len(word) >= 4 and "m" in word
    ]
    print(answers)
