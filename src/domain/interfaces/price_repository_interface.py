from abc import ABC, abstractmethod
from ..entities.price import Price

class IPriceRepositoryDB(ABC):
    @abstractmethod
    async def add(self, price: Price) -> None:
        pass

    @abstractmethod
    async def get_last(self, symbol: str) -> Price | None:
        pass