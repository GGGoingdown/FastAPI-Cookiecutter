import pytest
import asyncio
from httpx import AsyncClient

# Application
from app import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    return loop


@pytest.fixture
def app(event_loop):
    app = create_app()
    yield app
    app.container.unwire()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
