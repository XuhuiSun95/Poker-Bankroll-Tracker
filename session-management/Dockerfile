# Install uv
FROM python:3.13-slim AS develop
COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Copy the application into the container.
FROM develop AS builder
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Copy the environment, but not the source code
FROM python:3.13-slim
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder --chown=app:app /app /app

# Expose the port
EXPOSE 80

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["fastapi", "run", "--port", "80", "/app/session-management"]
