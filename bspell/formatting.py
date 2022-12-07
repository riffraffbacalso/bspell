import textwrap as tw

ANS_SEQ = "3;4"
PAN_SEQ = "38;5;2"
RST_SEQ = "\033[0m"


def render_lines(lines: list[str], answers: list[str]) -> list[str]:
    def is_answer(word: str) -> bool:
        return word in answers

    def is_pangram(word: str) -> bool:
        return len(set(word)) == 7

    def esc_seq(word: str) -> str:
        seq = "\033[1;" if is_pangram(word) or is_answer(word) else ""
        seq += ANS_SEQ if is_answer(word) else ""
        seq += ";" if is_pangram(word) and is_answer(word) else ""
        seq += PAN_SEQ if is_pangram(word) else ""
        seq += "m" if is_pangram(word) or is_answer(word) else ""
        seq += word
        seq += RST_SEQ if is_pangram(word) or is_answer(word) else ""
        return seq

    def render(line: str) -> str:
        return " ".join(esc_seq(word) for word in line.split())

    return [render(line) for line in lines]


def fprint(words: list[str], answers: list[str]) -> None:
    words = tw.wrap(" ".join(words))
    words = render_lines(words, answers)
    print(*(f"  {line}" for line in words), sep="\n")
