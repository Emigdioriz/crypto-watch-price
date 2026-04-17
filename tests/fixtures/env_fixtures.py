import pytest
from httpx import AsyncClient, ASGITransport

from infraestructure.config.db import get_session
from alert.main import app


@pytest.fixture()
async def client(session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client

    app.dependency_overrides.clear()