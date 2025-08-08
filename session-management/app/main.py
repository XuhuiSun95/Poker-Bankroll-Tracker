from importlib import metadata

from fastapi import FastAPI

app = FastAPI(
    title="session-management",
    version=metadata.version("session-management"),
)
