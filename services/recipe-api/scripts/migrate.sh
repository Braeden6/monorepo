#!/bin/bash
# Apply all pending migrations

uv run alembic upgrade head
