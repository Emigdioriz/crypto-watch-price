from fastapi import APIRouter, Depends, status
from httpx import AsyncClient
from typing import Annotated

from ....infraestructure.config.db import Session
from ....infraestructure.external.coingecko_client import CoinGeckoClient
from ....infraestructure.repositories.price_repository_db import PriceRepositoryDB
from ....application.use_cases.price_use_cases import GetPriceUseCase
from ....application.dtos.price_dtos import PriceResponseDTO
from ....application.dtos.common.api_dto import ApiResponse
from ....price.config.http import HttpClient

router = APIRouter(prefix="/price", tags=["prices"])


@router.get("/{symbol}", response_model=ApiResponse[PriceResponseDTO], status_code=status.HTTP_200_OK)
async def get_price(
    symbol: str,
    http_client: HttpClient,
    session: Session
):
    price_repository = PriceRepositoryDB(session)
    coingecko_client = CoinGeckoClient(http_client)
    get_price_use_case = GetPriceUseCase(repository=price_repository, client=coingecko_client)

    result = await get_price_use_case.execute(symbol)

    return ApiResponse(detail=result)