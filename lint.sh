#!/bin/bash
set -e

# Frontend
cd frontend
npm run format
npm run lint

# Backend
cd ../backend
uv run black --check .
uv run pylint .
uv run ruff check .
uv run mypy .
