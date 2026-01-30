import strawberry
from dapr.clients import DaprClient

from ...api.deps import IsAuthenticated
from ...models.enums import SessionStatus
from ...models.session import EndSession, Session, StartSession
from ...schemas.session import EndSessionInput, SessionType, StartSessionInput


@strawberry.type
class Query:
    @strawberry.field(
        graphql_type=SessionType | None,
        permission_classes=[IsAuthenticated],
    )  # type: ignore[misc]
    async def current_session(self, info: strawberry.Info) -> Session | None:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if state.data:
                return Session.model_validate_json(state.data)
        return None

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    async def has_current_session(self, info: strawberry.Info) -> bool:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if state.data:
                return True
        return False


@strawberry.type
class Mutation:
    @strawberry.field(
        graphql_type=SessionType,
        permission_classes=[IsAuthenticated],
    )  # type: ignore[misc]
    async def start_session(
        self,
        input: StartSessionInput,
        info: strawberry.Info,
    ) -> Session:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if state.data:
                raise Exception("Session already exists")
            session = StartSession(
                status=SessionStatus.ACTIVE,
                version=1,
                **strawberry.asdict(input),
            )
            client.save_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
                value=session.model_dump_json(),
                state_metadata={"ttlInSeconds": "172800"},
            )
            return session

    @strawberry.field(
        graphql_type=SessionType,
        permission_classes=[IsAuthenticated],
    )  # type: ignore[misc]
    async def end_session(
        self,
        input: EndSessionInput,
        info: strawberry.Info,
    ) -> Session:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if not state.data:
                raise Exception("No active session")
            session = Session.model_validate_json(state.data)
            if session.status == SessionStatus.ENDED:
                raise Exception("Session already ended")
            session = EndSession(
                **(session.model_dump(exclude_unset=True) | strawberry.asdict(input))
            )
            client.save_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
                value=session.model_dump_json(),
                state_metadata={"ttlInSeconds": "1800"},
            )
            return session

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    async def discard_session(self, info: strawberry.Info) -> bool:
        user_id = info.context["current_user"].sub
        with DaprClient() as client:
            state = client.get_state(
                store_name="redis-state-store",
                key=f"user:{user_id}",
            )
            if state.data:
                client.delete_state(
                    store_name="redis-state-store",
                    key=f"user:{user_id}",
                )
        return True
