from abc import ABC, abstractmethod
from ..entities.price import Price

class IPriceClientRepository(ABC):
    @abstractmethod
    async def get_price(self, symbol: str) -> Price:
        pass