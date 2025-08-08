#!/usr/bin/env bash
set -x

uv sync
pre-commit install
dapr init
