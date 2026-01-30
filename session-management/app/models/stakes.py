from pydantic import BaseModel, NonNegativeInt, PositiveInt


class GameStake(BaseModel):
    small_blind_cents: PositiveInt
    big_blind_cents: PositiveInt
    ante_cents: NonNegativeInt | None = 0
