import datetime

from pydantic import BaseModel


class Session(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
