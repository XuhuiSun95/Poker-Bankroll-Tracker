from typing import NewType

import strawberry
from pydantic_extra_types.coordinate import Latitude, Longitude
from pydantic_extra_types.currency_code import ISO4217

LatitudeScalar = strawberry.scalar(
    NewType("Latitude", float),
    name="Latitude",
    description=(
        """
        The `Latitude` scalar type presents constrained float value between -90 and 90
        """
    ),
)
LongitudeScalar = strawberry.scalar(
    NewType("Longitude", float),
    name="Longitude",
    description=(
        """
        The `Longitude` scalar type presents constrained float value between -180 and
        180
        """
    ),
)

ISO4217Scalar = strawberry.scalar(
    NewType("ISO4217", str),
    name="ISO4217",
    description=(
        """
        The `ISO4217` scalar type presents constrained string value of ISO 4217
        currency code
        """
    ),
)

scalars_mapping = {
    ISO4217: ISO4217Scalar,
    Latitude: LatitudeScalar,
    Longitude: LongitudeScalar,
}
