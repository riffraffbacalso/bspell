from concurrent.futures import ThreadPoolExecutor
from typing import ContextManager, Iterable, Iterator, TextIO, TypeVar

import httpx

T = TypeVar("T", str, bytes)


def file_gen(gen: Iterator, file: TextIO) -> Iterator:
    for it in gen:
        file.write(f"{it}\n")
        yield it
    file.close()


def chain_gen(gens: Iterable[Iterator[T]]) -> Iterator[T]:
    for gen in gens:
        for it in gen:
            yield it


def unique_gen(gen: Iterator[T]) -> Iterator[T]:
    seen = set()
    for it in gen:
        if it not in seen:
            yield it
            seen.add(it)


# TODO handle context exiting on exception


def stream_gen(
    gen: Iterator[T], stream_context: ContextManager[httpx.Response]
) -> Iterator[T]:
    for it in gen:
        yield it
    print(stream_context.__exit__(None, None, None))


def pool_gen(gen: Iterator[T], pool: ThreadPoolExecutor) -> Iterator[T]:
    for it in gen:
        yield it
    pool.__exit__(None, None, None)


def client_gen(gen: Iterator[T], client: httpx.Client) -> Iterator[T]:
    for it in gen:
        yield it
    client.close()
