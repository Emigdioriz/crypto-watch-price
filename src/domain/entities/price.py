
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, mapped_as_dataclass
from datetime import datetime

from ...infraestructure.config.db import mapper_registry

@mapped_as_dataclass(mapper_registry)
class Price:
    __tablename__ = "prices"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        init=False,
        default_factory=uuid4,
    )
    symbol: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    price_usd: Mapped[Decimal] = mapped_column(
        Decimal,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        init=False,
        nullable=False
    )