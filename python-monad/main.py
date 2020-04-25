import asyncio
from enum import Enum
from typing import Dict, Iterable, Any, List, Callable, Generic, TypeVar, Union

import aiohttp
from monads import Result, Ok, Err, Future

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class FutureResult(Generic[A, B]):
    def __init__(self, fut_res: Future[Result[A, B]]):
        self.fut_res = fut_res

    def map(self, fn: Callable[[A], Result[C, B]]) -> "FutureResult[A, B]":
        return FutureResult(self.fut_res.map(lambda res: res.map(fn)))

    def bind(self, fn: Callable[[A], "FutureResult[C, B]"]) -> "FutureResult[A, B]":
        return FutureResult(
            self.fut_res.bind(lambda r: fn(r.value).fut_res if isinstance(r, Ok) else Future.pure(Err(r.err)))
        )

    def __await__(self):
        return self.fut_res.__await__()


class ErrorEnum(Enum):
    BadUrl = 1
    IoError = 2
    InvalidResponse = 3


def check_url(url: str) -> Result[str, ErrorEnum]:
    return Ok(url) if "https://" in url else Err(ErrorEnum.BadUrl)


def download_url(url: str) -> Future[Result[aiohttp.ClientResponse, ErrorEnum]]:
    async def fn() -> Result[aiohttp.ClientResponse, ErrorEnum]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return Ok(resp)
        except:
            return Err(ErrorEnum.IoError)

    return Future(fn())


def validate_http_response(res: aiohttp.ClientResponse) -> Result[Dict[str, str], ErrorEnum]:
    if res.content_type != "application/json":
        return Err(ErrorEnum.InvalidResponse)
    if res.status >= 400:
        return Err(ErrorEnum.InvalidResponse)

    return Ok({
        "status": res.status,
        "header": str(res.headers.items())
    })


async def download_valid_url_and_validate(url: str) -> Result[Dict[str, str], ErrorEnum]:
    return await FutureResult(Future.pure(check_url(url)))\
            .bind(lambda u: FutureResult(download_url(u)))\
            .map(validate_http_response)


if __name__ == "__main__":
    print(asyncio.run(download_valid_url_and_validate("https://postman-echo.com/get?foo1=bar1&foo2=bar2")))