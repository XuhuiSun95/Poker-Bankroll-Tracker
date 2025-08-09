from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    scope: str
    name: str
    email: str
