import strawberry

from ..models.money import Money


@strawberry.experimental.pydantic.type(model=Money, all_fields=True)
class MoneyType:
    pass


@strawberry.experimental.pydantic.input(model=Money, all_fields=True)
class MoneyInput:
    pass
