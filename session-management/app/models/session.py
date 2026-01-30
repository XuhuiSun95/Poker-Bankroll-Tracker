import datetime as dt

from pydantic import BaseModel, Field, PositiveInt, model_validator

from .enums import GameType, SessionStatus
from .events import HandNote, Rebuy, StackUpdate
from .location import PlayerLocation
from .money import Money
from .stakes import GameStake


class Session(BaseModel):
    status: SessionStatus
    version: PositiveInt

    player_name: str
    player_location: PlayerLocation

    game_type: GameType
    game_stack: GameStake

    buy_in: Money

    start_time: dt.datetime
    stop_time: dt.datetime | None = None
    cashout_time: dt.datetime | None = None

    final_stack: Money | None = None
    live_stack: Money | None = None

    rebuys: list[Rebuy] = Field(default_factory=list)
    stack_updates: list[StackUpdate] = Field(default_factory=list)
    hand_notes: list[HandNote] = Field(default_factory=list)

    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    updated_at: dt.datetime = Field(default_factory=dt.datetime.now)


class StartSession(Session):
    @model_validator(mode="after")
    def init_live_stack(self):
        if not self.live_stack:
            self.live_stack = self.buy_in
        return self


class EndSession(Session):
    stop_time: dt.datetime
    cashout_time: dt.datetime

    final_stack: Money

    @model_validator(mode="after")
    def end_session_input_validator(self):
        if self.stop_time < self.start_time:
            raise ValueError("stop_time must be after start_time")
        if self.cashout_time < self.stop_time:
            raise ValueError("cashout_time must be after stop_time")
        if self.cashout_time < self.start_time:
            raise ValueError("cashout_time must be after start_time")
        if self.final_stack.currency != self.buy_in.currency:
            raise ValueError("final_stack currency must match buy_in currency")
        self.live_stack = self.final_stack
        self.stack_updates.append(
            StackUpdate(stack_amount=self.final_stack, at=self.cashout_time)
        )
        self.version += 1
        self.updated_at = dt.datetime.now()
        self.status = SessionStatus.ENDED
        return self


class SessionEvent(BaseModel):
    version: PositiveInt
    status: SessionStatus | None = None
    live_stack: Money | None = None
    rebuys: list[Rebuy] | None = None
    stack_updates: list[StackUpdate] | None = None
    hand_notes: list[HandNote] | None = None
    updated_at: dt.datetime = Field(default_factory=dt.datetime.now)
