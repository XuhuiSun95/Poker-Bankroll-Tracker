import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_query_session(client: AsyncClient) -> None:
    query = """
        query MyQuery {
          session {
            createdAt
            description
            id
            name
            updatedAt
          }
        }
    """
    response = await client.post(
        "/graphql",
        json={"query": query},
    )
    assert response.status_code == 200
    assert "session" in response.json()["data"]
    assert "createdAt" in response.json()["data"]["session"]
    assert "description" in response.json()["data"]["session"]
    assert "id" in response.json()["data"]["session"]
    assert "name" in response.json()["data"]["session"]
    assert "updatedAt" in response.json()["data"]["session"]


@pytest.mark.anyio
async def test_mutation_create_session(client: AsyncClient) -> None:
    mutation = """
        mutation MyMutation {
          createSession(name: "test") {
            id
            name
            createdAt
            description
            updatedAt
          }
        }
    """
    response = await client.post(
        "/graphql",
        json={"query": mutation},
    )
    assert response.status_code == 200
    assert "createSession" in response.json()["data"]
    assert "id" in response.json()["data"]["createSession"]
    assert response.json()["data"]["createSession"]["name"] == "test"
    assert "createdAt" in response.json()["data"]["createSession"]
    assert "description" in response.json()["data"]["createSession"]
    assert "updatedAt" in response.json()["data"]["createSession"]
