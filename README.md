# Fast API — Learning Portfolio

A personal learning repository where I practice the **FastAPI** framework by building a Todo CRUD API. It contains two parallel implementations of the same API to compare approaches.

## Implementations

### 1. In-Memory API — [`app/`](app/)
A simple FastAPI app that stores todos in a Python dictionary. Good for understanding routing, Pydantic validation, and HTTP methods without database setup.

### 2. SQLModel + SQLite API — [`day5/`](day5/)
The same API refactored to use **SQLModel** as the ORM with a SQLite database (`day5/todos.db`). Demonstrates dependency injection for sessions, lifespan events for table creation, and partial updates via `TodoUpdate`.

## Tech Stack

- **Python** 3.14
- **FastAPI** — web framework
- **Uvicorn** — ASGI server
- **Pydantic** — request/response validation
- **SQLModel** — ORM (day5 only)
- **SQLite** — database (day5 only)
- **uv** — Python package manager

## Getting Started

```sh
# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

### Run the In-Memory API (from repo root)
```sh
uv run main.py
```
API will be available at `http://localhost:8000` — interactive docs at `/docs`.

### Run the SQLModel API (from `day5/` directory)
```sh
cd day5
uv run main.py
```

## API Endpoints

Both implementations expose the same endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/todos` | Create a new todo |
| `GET` | `/todos` | List all todos |
| `GET` | `/todos/{id}` | Get a single todo |
| `PUT` | `/todos/{id}` | Update a todo |
| `DELETE` | `/todos/{id}` | Delete a todo |

A todo has three fields: `title`, `priority` (`low` / `medium` / `high`), and `is_done` (boolean).

## Purpose

This repo documents my progression as I learn FastAPI — from basic routing toward database integration, validation, and eventually authentication and file uploads.