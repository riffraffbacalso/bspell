# bspell

**bspell** is a solver for the New York Times daily puzzle game [Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee)

## The Game

Each puzzle is a list of seven letters in a honeycomb formation, for example:

```
 M O
P L B
 E R
```

The goal then is to find as many English words satisfying the following constraints:

- consists only of letters from the list
- is at least 4 letters long
- includes the centre letter
- is not a hyphenated word, proper noun, or profanity
- may contain the same letter more than once

Some answers for the above example are: "role", "bell", "people", or the pangram—a word including every letter—"problem"

## The Solver

**bspell** requires [Poetry](https://python-poetry.org/) and an installation of [Google Chrome](https://www.google.co.uk/chrome/) to work

To use, first clone this repository and run `poetry install` from root to create the virtual environment and install its dependencies. Then, create a shell with `poetry shell` and run `bspell` from the virtual environment, or run `poetry run bspell` to keep the current shell. **bspell** will fetch the day's puzzle and present its solutions

```
poetry shell
bspell
```

Answers are given in reverse word frequency order, meaning the more common a word's usage the earlier it will show, and pangrams will be highlighted in <span style="color:#98C379">**green**</span>

To manually input your own puzzle, just give a seven letter string as argument and it will forego fetching the puzzle to solve it. The first letter is taken to be the centre of the honeycomb, or the letter that must be included. The order of the remaining letters is irrelevant

```
bspell <puzzle string>
```

By default, **bspell** uses the pre-installed dictionary on Mac and Linux machines found in `usr/share/dict/words`. In some cases, this dictionary may be insufficient, in which case you may specify an alternative word source with the `-w` or `--word-source` argument. Currently the options are "OPTED", or the [Online Plain Text English Dictionary](https://www.mso.anu.edu.au/~ralph/OPTED/), and "chirico", a comprehensive word list compiled by [Mike Chirico](https://sourceforge.net/projects/souptonuts/files/souptonuts/dictionary/linuxwords.1.tar.gz/download). **bspell** will download the word list in the project directory, if not already there, and find solutions from it

```
bspell -w <word source>
```
