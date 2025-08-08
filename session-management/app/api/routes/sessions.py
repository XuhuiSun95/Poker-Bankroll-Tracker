import datetime
import uuid

import strawberry
from pydantic import BaseModel


class Session(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type(name="Session")
class SessionType:
    id: strawberry.ID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type
class Query:
    @strawberry.field(graphql_type=SessionType)  # type: ignore[misc]
    def session(self) -> Session:
        return Session(
            id=str(uuid.uuid4()),
            name="test",
            description="test",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )


@strawberry.type
class Mutation:
    @strawberry.field(graphql_type=SessionType)  # type: ignore[misc]
    def create_session(self, name: str) -> Session:
        return Session(
            id=str(uuid.uuid4()),
            name=name,
            description="test",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
