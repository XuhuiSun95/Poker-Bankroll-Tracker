import strawberry

from ..models.location import GeoPoint, PlayerLocation


@strawberry.experimental.pydantic.type(model=GeoPoint, all_fields=True)
class GeoPointType:
    pass


@strawberry.experimental.pydantic.input(model=GeoPoint, all_fields=True)
class GeoPointInput:
    pass


@strawberry.experimental.pydantic.type(model=PlayerLocation, all_fields=True)
class PlayerLocationType:
    pass


@strawberry.experimental.pydantic.input(model=PlayerLocation, all_fields=True)
class PlayerLocationInput:
    pass
