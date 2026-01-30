from collections.abc import Iterator
from typing import Annotated, Any

import strawberry
from fastapi import APIRouter, Depends
from graphql.error import GraphQLError
from graphql.execution import ExecutionResult
from pydantic import ValidationError
from strawberry.extensions import SchemaExtension
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from ..models.token import TokenPayload
from ..schemas.scalar import scalars_mapping
from .deps import get_current_oidc_user, get_current_oidc_user_graphql_context
from .routes import sessions

query = merge_types("Query", (sessions.Query,))
mutation = merge_types("Mutation", (sessions.Mutation,))


class PydanticValidationExtension(SchemaExtension):
    def parse_validation_error(self, error: GraphQLError) -> GraphQLError:
        if isinstance(error.original_error, ValidationError):
            return GraphQLError(
                message=" ".join(
                    [error["msg"] for error in error.original_error.errors()]
                ),
                nodes=error.nodes,
                source=error.source,
                positions=error.positions,
                path=error.path,
                original_error=error.original_error,
            )
        return error

    def _process_result(self, result: Any) -> None:
        if not result.errors:
            return

        processed_errors: list[GraphQLError] = []

        for error in result.errors:
            processed_errors.append(self.parse_validation_error(error))

        result.errors = processed_errors

    def on_operation(self) -> Iterator[None]:
        yield

        result = self.execution_context.result

        if isinstance(result, ExecutionResult):
            self._process_result(result)
        elif result:
            self._process_result(result.initial_result)


schema = strawberry.Schema(
    query=query,
    mutation=mutation,
    scalar_overrides=scalars_mapping,  # type: ignore[arg-type]
    extensions=[PydanticValidationExtension()],
)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_current_oidc_user_graphql_context,  # type: ignore[arg-type]
)

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
