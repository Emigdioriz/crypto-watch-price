# from contextlib import contextmanager
# from datetime import datetime
# import pytest
# from sqlalchemy.pool import NullPool
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy import event
# from infraestructure.config.db import mapper_registry
# from infraestructure.config.env import TestSettings


# @pytest.fixture(scope="session")
# async def engine():
#     engine = create_async_engine(str(TestSettings().database_url), poolclass=NullPool)
#     yield engine


# @pytest.fixture
# async def session(engine):
#     async with engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.create_all)
    
#     async with AsyncSession(engine, expire_on_commit=False) as session:
#         yield session
    
#     async with engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)


# @contextmanager
# def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
#     def fake_time_handler(mapper, connection, target):
#         if hasattr(target, 'created_at'):
#             target.created_at = time
#         if hasattr(target, 'updated_at'):
#             target.updated_at = time

#     event.listen(model, 'before_insert', fake_time_handler)

#     yield time

#     event.remove(model, 'before_insert', fake_time_handler)


# @pytest.fixture
# def mock_db_time():
#     return _mock_db_time


import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.infraestructure.config.db import mapper_registry, get_session
from fastapi.testclient import TestClient
from src.main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    await engine.dispose()


@pytest.fixture
def client():
    # Cria engine ASYNC em memória para usar com TestClient
    # TestClient executa endpoints async normalmente
    # Engine async com SQLite em memória
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
    
    # Cria as tabelas de forma síncrona (necessário para setup da fixture)
    async def setup_db():
        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.create_all)
    
    asyncio.run(setup_db())
    
    # Função de override que retorna AsyncSession
    async def get_test_session():
        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session
    
    app.dependency_overrides[get_session] = get_test_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides = {}
    
    # Cleanup
    async def cleanup():
        await engine.dispose()
    
    asyncio.run(cleanup()) 