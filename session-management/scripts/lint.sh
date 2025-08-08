#!/usr/bin/env bash
set -e
set -x

uv run mypy app
uv run ruff check
uv run ruff format --check
