from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import registry
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from .env import Settings, get_settings


mapper_registry = registry()
metadata = mapper_registry.metadata
engine = None


def create_engine(settings: Settings):
    global engine
    if engine is None:
        engine = create_async_engine(str(settings.database_url), echo=settings.debug)
    
    return engine


async def get_session(settings: Annotated[Settings, Depends(get_settings)]):
    engine = create_engine(settings)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]