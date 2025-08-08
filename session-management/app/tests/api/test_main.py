import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_liveness(client: AsyncClient) -> None:
    response = await client.get("/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_readiness(client: AsyncClient) -> None:
    response = await client.get("/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
