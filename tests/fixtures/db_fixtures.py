from contextlib import contextmanager
from datetime import datetime
import pytest
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import event
from {{project_name}}.config.db import mapper_registry
from {{project_name}}.config.env import TestSettings


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(str(TestSettings().database_url), poolclass=NullPool)
    yield engine


@pytest.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time