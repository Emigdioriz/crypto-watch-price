from sqlalchemy import select

from ...domain.entities.price import Price
from ...domain.interfaces.price_repository_interface import IPriceRepositoryDB
from ..common.services.db_utils import find_one_or_fail


class PriceRepositoryDB(IPriceRepositoryDB):
    def __init__(self, session):
        self._session = session

    async def add(self, price: Price) -> None:
        self._session.add(price)
        await self._session.commit()

    async def get_last(self, symbol: str) -> Price | None:
        result = await find_one_or_fail(
            query=select(Price).where(Price.symbol == symbol).order_by(Price.created_at.desc()),
            session=self._session,
            error_message=f"Price not found for symbol: {symbol}"
        )
        return result