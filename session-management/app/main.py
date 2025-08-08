from importlib import metadata

from fastapi import FastAPI

from .api.main import api_router

app = FastAPI(
    title="session-management",
    version=metadata.version("session-management"),
)
app.include_router(api_router)
