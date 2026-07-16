#!/bin/bash
set -e

# Frontend
cd frontend
npm run format
npm run lint

# Backend
cd ../backend
uv run black .
uv run pylint .
uv run ruff check .
