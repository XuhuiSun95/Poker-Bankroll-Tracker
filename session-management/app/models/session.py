import datetime as dt

from pydantic import BaseModel, Field, NonNegativeInt

from .enums import GameType, SessionStatus
from .events import HandNote, Rebuy, StackUpdate
from .location import PlayerLocation
from .money import Money
from .stakes import GameStake


class Session(BaseModel):
    status: SessionStatus
    version: NonNegativeInt

    player_name: str
    player_location: PlayerLocation

    game_type: GameType
    game: GameStake

    buy_in: Money

    start_time: dt.datetime
    stop_time: dt.datetime | None = None
    cashout_time: dt.datetime | None = None

    final_stack: Money | None = None
    live_stack: Money | None = None

    rebuys: list[Rebuy] = Field(default_factory=list)
    stack_updates: list[StackUpdate] = Field(default_factory=list)
    hand_notes: list[HandNote] = Field(default_factory=list)

    created_at: dt.datetime
    updated_at: dt.datetime


class SessionEvent(BaseModel):
    version: NonNegativeInt
    status: SessionStatus | None = None
    live_stack: Money | None = None
    rebuys: list[Rebuy] | None = None
    stack_updates: list[StackUpdate] | None = None
    hand_notes: list[HandNote] | None = None
    updated_at: dt.datetime
