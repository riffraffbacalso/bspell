from functools import wraps
import sys
from typing import Any, Callable

from retry import retry
import httpx


def retry_msg(msg: str) -> Callable:
    def retry_http(func: Callable) -> Callable:
        @retry(httpx.TransportError, tries=5, delay=1)
        def retry_func(*args: tuple[Any, ...]):
            return func(*args)

        @wraps(retry_func)
        def retry_catch_exit_func(*args: tuple[Any, ...]) -> Callable:
            try:
                return retry_func(*args)
            except httpx.TransportError as err:
                sys.exit(f"{type(err).__name__}: {err}\n{msg}")

        return retry_catch_exit_func

    return retry_http
