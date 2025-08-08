import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from .routes import sessions

query = merge_types("Query", (sessions.Query,))
mutation = merge_types("Mutation", (sessions.Mutation,))

schema = strawberry.Schema(query=query, mutation=mutation)
graphql_app = GraphQLRouter(schema)

api_router = APIRouter()
api_router.include_router(graphql_app, prefix="/graphql")


@api_router.get("/liveness")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/readiness")
async def readiness() -> dict[str, str]:
    return {"status": "ok"}
