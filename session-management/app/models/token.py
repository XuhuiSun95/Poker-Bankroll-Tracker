from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    scope: str
    name: str
    email: str


class TokenPayloadError(BaseModel):
    status_code: int
    detail: str
    headers: dict[str, str]
