import strawberry

from ..models.session import Session
from .stakes import GameStakeType


@strawberry.experimental.pydantic.type(model=Session)
class SessionType:
    status: strawberry.auto
    version: strawberry.auto

    player_name: strawberry.auto
    player_location: strawberry.auto

    game_type: strawberry.auto
    game: GameStakeType

    buy_in: strawberry.auto

    start_time: strawberry.auto
    stop_time: strawberry.auto
    cashout_time: strawberry.auto

    final_stack: strawberry.auto
    live_stack: strawberry.auto

    rebuys: strawberry.auto
    stack_updates: strawberry.auto
    hand_notes: strawberry.auto

    created_at: strawberry.auto
    updated_at: strawberry.auto
