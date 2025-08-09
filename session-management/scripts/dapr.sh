#!/usr/bin/env bash
set -x

dapr run --app-id session-management --app-port 8000 --components-path ./components -- uv run fastapi dev
