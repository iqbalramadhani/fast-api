# Todo API

Simple CRUD API built with FastAPI + SQLModel, as part of learning 
backend development in Python after 6 years as a PHP developer.

## Tech Stack
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- uv (package manager)

## Features
- Create, read, update, delete todos
- Request/response validation with Pydantic
- Environment-based configuration
- Auto-generated API docs (Swagger)

## Setup

1. Clone this repo
2. Install dependencies:
   \`\`\`
   uv sync
   \`\`\`
3. Copy environment file:
   \`\`\`
   cp .env.example .env
   \`\`\`
4. Run the server:
   \`\`\`
   uv run uvicorn main:app --reload
   \`\`\`
5. Open http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /todos | Create a new todo |
| GET | /todos | List all todos |
| GET | /todos/{id} | Get a single todo |
| PUT | /todos/{id} | Update a todo |
| DELETE | /todos/{id} | Delete a todo |

## What I learned
- FastAPI routing, path/query parameters, type hints
- Pydantic models for request/response validation
- SQLModel for ORM (table models vs schema models)
- Dependency injection pattern (`Depends`)
- Environment variable management
- Lifespan events (replacing deprecated `on_event`)