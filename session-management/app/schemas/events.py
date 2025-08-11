import strawberry

from ..models.events import HandNote, Rebuy, StackUpdate
from .money import (
    MoneyInput,  # noqa: F401
    MoneyType,  # noqa: F401
)


@strawberry.experimental.pydantic.type(model=Rebuy, all_fields=True)
class RebuyType:
    pass


@strawberry.experimental.pydantic.type(model=StackUpdate, all_fields=True)
class StackUpdateType:
    pass


@strawberry.experimental.pydantic.type(model=HandNote, all_fields=True)
class HandNoteType:
    pass
