from pydantic import BaseModel, NonNegativeInt, PositiveInt


class CashStake(BaseModel):
    small_blind_cents: PositiveInt
    big_blind_cents: PositiveInt
    ante_cents: NonNegativeInt | None = 0


class TournamentStake(BaseModel):
    small_blind_cents: PositiveInt | None = None
    big_blind_cents: PositiveInt | None = None
    ante_cents: NonNegativeInt | None = None


GameStake = CashStake | TournamentStake
