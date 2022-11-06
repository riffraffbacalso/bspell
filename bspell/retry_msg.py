from typing import Any, Callable
from retry import retry
import httpx


def retry_msg(msg: str):
    def retry_http(func: Callable) -> Callable:
        @retry(httpx.TransportError, tries=5, delay=1)
        def retry_func(*args: tuple[Any, ...]):
            return func(*args)

        def retry_catch_exit_func(*args: tuple[Any, ...]):
            try:
                return retry_func(*args)
            except httpx.TransportError as err:
                raise SystemExit(f'{msg} {str(type(err))[8:-2]}: "{err}"')

        return retry_catch_exit_func

    return retry_http