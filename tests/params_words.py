OS_PARAMS = {
    "4 letters or more": (
        ["q", "qw", "qwe", "qwer", "qwert", "qwerty", "qwertyu"],
        ["qwer", "qwert", "qwerty", "qwertyu"],
    ),
    "strip newlines": (
        ["wer\n", "wert\n", "werty\n", "wertyu\n", "wertyui\n"],
        ["wert", "werty", "wertyu", "wertyui"],
    ),
    "lowercase": (
        ["ERT", "ERTY", "ERTYU", "ERTYUI", "ERTYUIO"],
        ["erty", "ertyu", "ertyui", "ertyuio"],
    ),
}

ALT_WS_PARAMS = {"OPTED": "OPTED", "chirico": "chirico"}

OPTED_PARAMS = {
    "word": ("Word", "n.", "A unit of language"),
    "tested": ("Tested", "imp. & p. p.", "Verified"),
    "fun": ("Fun", "n.", "Amusement"),
}

TAR_PARAMS = {
    "4 letters or more": (
        "datum\ndata\ndap",
        ["datum", "data"],
    ),
    "lowercase": (
        "Lower\nCASE\nLeTtErInG",
        ["lower", "case", "lettering"],
    ),
    "accent": (
        "café\nfaçade\njalapeño\nnaïve",
        ["cafe", "facade", "jalapeno", "naive"],
    ),
    "apostrophe": (
        "it's\ntheirs\nhers\njoe's",
        ["theirs", "hers"],
    ),
}

PRINT_PARAMS = {
    "qwerty": ["q", "w", "e", "r", "t", "y"],
    "abcdef": ["a", "b", "c", "d", "e", "f"],
}
