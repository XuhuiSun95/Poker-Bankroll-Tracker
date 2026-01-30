import strawberry

from ..models.stakes import GameStake


@strawberry.experimental.pydantic.type(model=GameStake, all_fields=True)
class GameStakeType:
    pass


@strawberry.experimental.pydantic.input(model=GameStake, all_fields=True)
class GameStakeInput:
    pass
