from typing import Annotated

import strawberry
from fastapi import APIRouter, Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from ..models.token import TokenPayload
from ..schemas.scalar import scalars_mapping
from .deps import get_current_oidc_user
from .routes import sessions

query = merge_types("Query", (sessions.Query,))
mutation = merge_types("Mutation", (sessions.Mutation,))

schema = strawberry.Schema(
    query=query,
    mutation=mutation,
    scalar_overrides=scalars_mapping,  # type: ignore[arg-type]
)
graphql_app = GraphQLRouter(schema)

api_router = APIRouter()
api_router.include_router(graphql_app, prefix="/graphql")


@api_router.get("/liveness")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/readiness")
async def readiness() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/sub")
async def sub(
    current_user: Annotated[TokenPayload, Depends(get_current_oidc_user)],
) -> dict[str, str]:
    return {"sub": current_user.sub}


@api_router.get("/scope")
async def scope(
    current_user: Annotated[TokenPayload, Depends(get_current_oidc_user)],
) -> dict[str, str]:
    return {"scope": current_user.scope}
