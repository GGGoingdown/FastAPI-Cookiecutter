import pytest
import asyncio
from fastapi.testclient import TestClient
from tortoise import Tortoise, generate_schema_for_client

# Application
from app import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    return loop


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests(event_loop, request):
    from app.db import get_tortoise_config

    TORTOISE_TEST_ORM = get_tortoise_config()
    await Tortoise.init(config=TORTOISE_TEST_ORM)
    await Tortoise.generate_schemas()
    await generate_schema_for_client(Tortoise.get_connection("default"), safe=True)


@pytest.fixture()
def app(event_loop):
    app = create_app()
    yield app
    app.container.unwire()


@pytest.fixture()
def client(app):
    yield TestClient(app)
