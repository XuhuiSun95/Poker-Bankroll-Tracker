from importlib import metadata

from fastapi import FastAPI

from .api.main import api_router
from .core.config import settings

app = FastAPI(
    title="session-management",
    version=metadata.version("session-management"),
    swagger_ui_init_oauth={
        "clientId": settings.OIDC_CLIENT_ID,
        "usePkceWithAuthorizationCodeGrant": True,
    },
)
app.include_router(api_router)
