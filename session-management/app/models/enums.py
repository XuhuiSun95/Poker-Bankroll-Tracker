from enum import Enum


class GameType(str, Enum):
    CASH_GAME = "CASH_GAME"
    TOURNAMENT = "TOURNAMENT"


class SessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class LocationSource(str, Enum):
    USER_INPUT = "USER_INPUT"
    GEOIP = "GEOIP"
    PLACE_PICKER = "PLACE_PICKER"
    OTHER = "OTHER"
