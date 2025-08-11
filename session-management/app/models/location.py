from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude

from .enums import LocationSource


class GeoPoint(BaseModel):
    latitude: Latitude
    longitude: Longitude


class PlayerLocation(BaseModel):
    display_name: str | None = None
    geo: GeoPoint | None = None
    address: str | None = None
    place_id: str | None = None
    source: LocationSource | None = None
