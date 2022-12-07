import textwrap as tw

ANS_SEQ = "3;4"
PAN_SEQ = "38;5;2"
RST_SEQ = "\033[0m"


def render_lines(lines: list[str], answers: list[str]) -> list[str]:
    def esc_seq(word: str) -> str:
        is_answer = word in answers
        is_pangram = len(set(word)) == 7
        seq = "\033[1;" if is_pangram or is_answer else ""
        seq += ANS_SEQ if is_answer else ""
        seq += ";" if is_pangram and is_answer else ""
        seq += PAN_SEQ if is_pangram else ""
        seq += "m" if is_pangram or is_answer else ""
        seq += word
        seq += RST_SEQ if is_pangram or is_answer else ""
        return seq

    def render(line: str) -> str:
        return " ".join(esc_seq(word) for word in line.split())

    return [render(line) for line in lines]


def fprint(words: list[str], answers: list[str]) -> None:
    words = tw.wrap(" ".join(words))
    words = render_lines(words, answers)
    print(*(f"  {line}" for line in words), sep="\n")
