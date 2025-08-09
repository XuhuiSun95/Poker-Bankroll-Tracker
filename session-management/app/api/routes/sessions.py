import datetime

import strawberry

from ...models.enums import GameType, LocationSource, SessionStatus
from ...models.location import GeoPoint, PlayerLocation
from ...models.money import Money
from ...models.session import Session
from ...models.stakes import CashStake, TournamentStake
from ...schemas import SessionType


@strawberry.type
class Query:
    @strawberry.field(graphql_type=SessionType)  # type: ignore[misc]
    def session(self) -> Session:
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


@strawberry.type
class Mutation:
    @strawberry.field(graphql_type=SessionType)  # type: ignore[misc]
    def create_session(self, name: str) -> Session:
        return Session(
            status=SessionStatus.ACTIVE,
            version=0,
            player_name=name,
            player_location=PlayerLocation(
                display_name="test",
                geo=GeoPoint(latitude=0, longitude=0),
                address="test",
                place_id="test",
                source=LocationSource.GEOIP,
            ),
            game_type=GameType.TOURNAMENT,
            game=TournamentStake(),
            buy_in=Money(amount_cents=100, currency="USD"),
            start_time=datetime.datetime.now(),
            stop_time=None,
            cashout_time=None,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
