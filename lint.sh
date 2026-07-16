#!/bin/bash
set -e

cd frontend
npm run format
npm run lint

cd ../backend
uv run black --check .
uv run pylint .
uv run ruff check .
