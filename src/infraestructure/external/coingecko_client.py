from datetime import datetime
import httpx
from fastapi import HTTPException, status

from ...domain.entities.price import Price
from ...domain.interfaces.price_client_repository import IPriceClientRepository

class CoinGeckoClient(IPriceClientRepository):
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client

    async def get_price(self, symbol: str) -> Price:
        response  = await self._http_client.get(
            self.BASE_URL,
            params={
                "ids": symbol,
                "vs_currencies": "usd"
            }
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to fetch price from CoinGecko"
            )
        
        data = response.json()
        if symbol not in data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Price for symbol '{symbol}' not found"
            )

        return Price(
            symbol=symbol,
            price_usd=data[symbol]["usd"],
        )