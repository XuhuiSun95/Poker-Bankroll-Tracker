import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_query_session(client: AsyncClient) -> None:
    query = """
        query MyQuery {
          session {
            status
            version
            playerName
            gameType
            buyIn { amountCents currency }
            createdAt
          }
        }
    """
    response = await client.post(
        "/graphql",
        json={"query": query},
    )
    assert response.status_code == 200
    data = response.json()["data"]["session"]
    assert data["playerName"] == "test"
    assert data["gameType"] == "CASH_GAME"
    assert data["buyIn"]["amountCents"] == 100
    assert data["buyIn"]["currency"] == "USD"
    assert "status" in data and "version" in data and "createdAt" in data


@pytest.mark.anyio
async def test_mutation_create_session(client: AsyncClient) -> None:
    mutation = """
        mutation MyMutation {
          createSession(name: "test") {
            playerName
            gameType
            playerLocation { displayName }
            createdAt
          }
        }
    """
    response = await client.post(
        "/graphql",
        json={"query": mutation},
    )
    assert response.status_code == 200
    data = response.json()["data"]["createSession"]
    assert data["playerName"] == "test"
    assert data["gameType"] == "TOURNAMENT"
    assert data["playerLocation"]["displayName"] == "test"
    assert "createdAt" in data
