import asyncio
from enum import Enum
from typing import Dict

import aiohttp
from monads import Result, Ok, Err, Future


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

    return Future(fn)


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
    pass  # We need a monad transformer


if __name__ == "__main__":
    asyncio.run(download_valid_url_and_validate("https://postman-echo.com/get?foo1=bar1&foo2=bar2"))