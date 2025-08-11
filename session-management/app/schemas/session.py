import strawberry

from ..models.session import (
    EndSession,
    Session,
    StartSession,
)
from .events import HandNoteType, RebuyType, StackUpdateType  # noqa: F401
from .location import GeoPointType, PlayerLocationType  # noqa: F401
from .money import MoneyInput, MoneyType  # noqa: F401
from .stakes import GameStakeInput, GameStakeType  # noqa: F401


@strawberry.experimental.pydantic.type(model=Session, all_fields=True)
class SessionType:
    pass


@strawberry.experimental.pydantic.input(model=StartSession)
class StartSessionInput:
    player_name: strawberry.auto
    player_location: strawberry.auto

    game_type: strawberry.auto
    game_stack: strawberry.auto

    buy_in: strawberry.auto

    start_time: strawberry.auto


@strawberry.experimental.pydantic.input(model=EndSession)
class EndSessionInput:
    stop_time: strawberry.auto
    cashout_time: strawberry.auto
    final_stack: strawberry.auto
