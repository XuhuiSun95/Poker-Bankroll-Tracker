from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from ..main import app


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
