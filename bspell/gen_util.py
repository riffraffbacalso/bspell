from concurrent.futures import ThreadPoolExecutor
from contextlib import _GeneratorContextManager
from string import ascii_lowercase
from typing import Callable, Iterator, TextIO, Type, TypeVar
import os

import httpx

_T = TypeVar("_T", str, bytes)
T = Type[_T]


def chain_iter(gens: list[Iterator[T]]) -> Iterator[T]:
    for gen in gens:
        for it in gen:
            yield it


def unique_iter(gen: Iterator[T]) -> Iterator[T]:
    seen = set()
    for it in gen:
        if it not in seen:
            yield it
            seen.add(it)


def file_iter(gen: Callable[[], Iterator[T]], file: TextIO) -> Iterator[T]:
    try:
        for it in gen():
            file.write(f"{it}\n")
            yield it
    except (Exception, SystemExit):
        file.close()
        os.remove(file.name)
        raise
    else:
        file.close()


def stream_iter(res_context: _GeneratorContextManager[httpx.Response]) -> Iterator[str]:
    try:
        res = res_context.__enter__()
        for it in res.iter_lines():
            yield it
    except (Exception, SystemExit) as err:
        res_context.__exit__(type(err), err, err.__traceback__)
        raise
    else:
        res_context.__exit__(None, None, None)


def pool_iter(
    pool: ThreadPoolExecutor, req_fun: Callable[[str], Iterator[str]]
) -> Iterator[str]:
    try:
        gens = list(pool.map(req_fun, ascii_lowercase))
        for it in chain_iter(gens):
            yield it
    finally:
        pool.shutdown()


def client_iter(gen: Iterator[T], client: httpx.Client) -> Iterator[T]:
    try:
        for it in gen:
            yield it
    finally:
        client.close()
