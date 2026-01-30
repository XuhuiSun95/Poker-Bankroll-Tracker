import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_query_current_session_initially_none(client: AsyncClient) -> None:
    query = """
        query GetOne { currentSession { status version playerName } }
    """
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["currentSession"] is None


@pytest.mark.anyio
async def test_start_session_then_query(client: AsyncClient) -> None:
    mutation = """
        mutation Start {
          startSession(
            input: {
              playerName: "Alice"
              playerLocation: { displayName: "Bellagio" }
              gameType: CASH_GAME
              gameStack: { smallBlindCents: 100, bigBlindCents: 200, anteCents: 0 }
              buyIn: { amountCents: 20000, currency: "USD" }
              startTime: "2025-08-09T16:30:00Z"
            }
          ) {
            status
            version
            playerName
            gameType
            buyIn
            { amountCents currency }
            createdAt
          }
        }
    """
    response = await client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    data = response.json()["data"]["startSession"]
    assert data["playerName"] == "Alice"
    assert data["gameType"] == "CASH_GAME"
    assert data["buyIn"]["amountCents"] == 20000
    assert data["buyIn"]["currency"] == "USD"

    # hasCurrentSession should be true
    query_has = """
        query Has { hasCurrentSession }
    """
    has_resp = await client.post("/graphql", json={"query": query_has})
    assert has_resp.status_code == 200
    assert has_resp.json()["data"]["hasCurrentSession"] is True

    # currentSession should now return data
    query_current = """
        query GetOne {
          currentSession {
            status version playerName gameType buyIn { amountCents currency }
          }
        }
    """
    current_resp = await client.post("/graphql", json={"query": query_current})
    assert current_resp.status_code == 200
    assert current_resp.json()["data"]["currentSession"]["playerName"] == "Alice"


@pytest.mark.anyio
async def test_end_session_then_discard(client: AsyncClient) -> None:
    # End session
    mutation_end = """
        mutation End {
          endSession(
            input: {
              stopTime: "2025-08-09T22:30:00Z"
              cashoutTime: "2025-08-09T22:40:00Z"
              finalStack: { amountCents: 31000, currency: "USD" }
            }
          ) {
            status
            stopTime
            cashoutTime
            finalStack { amountCents currency }
          }
        }
    """
    end_resp = await client.post("/graphql", json={"query": mutation_end})
    assert end_resp.status_code == 200
    end_data = end_resp.json()["data"]["endSession"]
    assert end_data["finalStack"]["amountCents"] == 31000

    # Discard session
    mutation_discard = """
        mutation Discard { discardSession }
    """
    discard_resp = await client.post("/graphql", json={"query": mutation_discard})
    assert discard_resp.status_code == 200
    assert discard_resp.json()["data"]["discardSession"] is True

    # Now currentSession should be null
    query_current = """
        query GetOne { currentSession { playerName } }
    """
    current_resp = await client.post("/graphql", json={"query": query_current})
    assert current_resp.status_code == 200
    assert current_resp.json()["data"]["currentSession"] is None
