from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient


async def get_http_client() -> AsyncClient:
    async with AsyncClient() as client:
        yield client
    
HttpClient = Annotated[AsyncClient, Depends(get_http_client)]