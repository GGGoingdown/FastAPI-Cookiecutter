import pytest

ENDPOINT = "/health"


@pytest.mark.asyncio
async def test_health_check(client):
    r = client.get(ENDPOINT)
    assert r.status_code == 200, f"Error status code: {r.json()}"
