WS_PARAMS = {
    "OS": "OS",
    "OPTED": "OPTED",
    "chirico": "chirico",
}

WL_PARAMS = {
    "only letters from puzzle": (
        ["qwer", "tqer", "yuqt", "uioq", "qopa", "aqop"],
        ["qwer", "tqer", "yuqt"],
    ),
    "4 letters or more": (
        ["q", "qw", "qwe", "qwer", "qwert", "qwerty", "qwertyu"],
        ["qwer", "qwert", "qwerty", "qwertyu"],
    ),
    "includes first letter": (
        ["qwer", "wert", "erty", "rtyq"],
        ["qwer", "rtyq"],
    ),
}
