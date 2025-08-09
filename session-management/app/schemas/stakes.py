import strawberry

from ..models.stakes import CashStake, TournamentStake


@strawberry.experimental.pydantic.type(model=CashStake, all_fields=True)
class CashStakeType:
    pass


@strawberry.experimental.pydantic.type(model=TournamentStake, all_fields=True)
class TournamentStakeType:
    pass


GameStakeType = strawberry.union("GameStakeType", (CashStakeType, TournamentStakeType))
