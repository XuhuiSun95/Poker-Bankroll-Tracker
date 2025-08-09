import datetime

import strawberry
from dapr.clients import DaprClient

from ...api.deps import IsAuthenticated
from ...models.enums import GameType, LocationSource, SessionStatus
from ...models.location import GeoPoint, PlayerLocation
from ...models.money import Money
from ...models.session import Session
from ...models.stakes import CashStake, TournamentStake
from ...schemas import SessionType


@strawberry.type
class Query:
    @strawberry.field(
        graphql_type=SessionType | None,
        permission_classes=[IsAuthenticated],
    )  # type: ignore[misc]
    async def current_session(self, info: strawberry.Info) -> Session | None:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if state.data:
                return Session.model_validate_json(state.data)
        return None

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    async def has_current_session(self, info: strawberry.Info) -> bool:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if state.data:
                return True
        return False


@strawberry.type
class Mutation:
    @strawberry.field(
        graphql_type=SessionType,
        permission_classes=[IsAuthenticated],
    )  # type: ignore[misc]
    async def start_session(
        self,
        player_name: str,
        player_location_display_name: str,
        game_type: GameType,
        info: strawberry.Info,
    ) -> Session:
        user_id = info.context["current_user"].sub
        stake = (
            CashStake(small_blind_cents=100, big_blind_cents=200, ante_cents=0)
            if game_type == GameType.CASH_GAME
            else TournamentStake()
        )
        session = Session(
            status=SessionStatus.ACTIVE,
            version=0,
            player_name=player_name,
            player_location=PlayerLocation(
                display_name=player_location_display_name,
                geo=GeoPoint(latitude=0, longitude=0),
                address=None,
                place_id=None,
                source=LocationSource.USER_INPUT,
            ),
            game_type=game_type,
            game=stake,
            buy_in=Money(amount_cents=20000, currency="USD"),
            start_time=datetime.datetime.now(),
            stop_time=None,
            cashout_time=None,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        with DaprClient() as client:
            client.save_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
                value=session.model_dump_json(),
            )
        return session
