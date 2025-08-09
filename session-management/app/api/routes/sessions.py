import datetime

import strawberry

from ...api.deps import IsAuthenticated
from ...models.enums import GameType, LocationSource, SessionStatus
from ...models.location import GeoPoint, PlayerLocation
from ...models.money import Money
from ...models.session import Session
from ...models.stakes import CashStake, TournamentStake
from ...schemas import SessionType


@strawberry.type
class Query:
    @strawberry.field(graphql_type=SessionType, name="currentSession")  # type: ignore[misc]
    def current_session(self) -> Session:
        # For now, return the same demo payload as `session`
        return Session(
            status=SessionStatus.ACTIVE,
            version=0,
            player_name="test",
            player_location=PlayerLocation(
                display_name="test",
                geo=GeoPoint(latitude=-33.8688, longitude=151.2093),
                address="test",
                place_id="test",
                source=LocationSource.GEOIP,
            ),
            game_type=GameType.CASH_GAME,
            game=CashStake(small_blind_cents=100, big_blind_cents=200, ante_cents=0),
            buy_in=Money(amount_cents=100, currency="USD"),
            start_time=datetime.datetime.now(),
            stop_time=None,
            cashout_time=None,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

    @strawberry.field(name="hasCurrentSession", permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def has_current_session(self, info: strawberry.Info) -> bool:
        user_id = info.context["current_user"].sub
        print(user_id)
        # Stubbed as true for demo; will reflect Redis state later
        return True


@strawberry.type
class Mutation:
    @strawberry.field(graphql_type=SessionType, name="startSession")  # type: ignore[misc]
    def start_session(
        self,
        player_name: str,
        player_location_display_name: str,
        game_type: GameType,
    ) -> Session:
        # Minimal stub matching README start example (truncated args for demo)
        stake = (
            CashStake(small_blind_cents=100, big_blind_cents=200, ante_cents=0)
            if game_type == GameType.CASH_GAME
            else TournamentStake()
        )
        return Session(
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
