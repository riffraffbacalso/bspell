from typing import Iterator, TextIO


def file_gen(gen: Iterator[str], file: TextIO) -> Iterator[str]:
    while True:
        try:
            word = next(gen)
            file.write(f"{word}\n")
            yield word
        except StopIteration:
            file.close()
            break

# TODO chain_gen (concatenate generators, replace itertools.chain which uses splat tuple)
# TODO unique_gen (delete duplicates, replace dict.fromkeys which creates dict)
# TODO stream_gen (close stream, client, and executor, allows return without exiting context)
