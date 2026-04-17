from decimal import Decimal

from ...application.dtos.price_dtos import PriceResponseDTO
from ...domain.interfaces.price_client_repository import IPriceClientRepository
from ...domain.interfaces.price_repository_interface import IPriceRepositoryDB


class BasePriceUseCase:
    def __init__(self, repository: IPriceRepositoryDB, client: IPriceClientRepository):
        self._repository = repository
        self._client = client

class GetPriceUseCase(BasePriceUseCase):
    async def execute(self, symbol: str) -> PriceResponseDTO:
        price = await self._client.get_price(symbol)
        await self._repository.add(price)
        return PriceResponseDTO(
            symbol=price.symbol,
            price_usd=Decimal(price.price_usd)
        )