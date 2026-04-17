from datetime import datetime
from ...application.dtos.common.response_dto import BaseResponse

class PriceResponseDTO(BaseResponse):
    symbol: str
    price_usd: float