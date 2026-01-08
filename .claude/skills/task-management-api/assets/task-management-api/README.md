# Task Management API

A production-ready Task Management REST API built with **FastAPI + SQLModel + UV** using **Test-Driven Development (TDD)**.

## Features

- Full CRUD operations (Create, Read, Update, Delete)
- Task priority levels (low, medium, high, urgent)
- Task status tracking (pending, in_progress, completed, cancelled)
- Due date management
- Pagination support
- **Neon Serverless PostgreSQL** support (with SQLite fallback)
- Comprehensive test suite with pytest

## Quick Start

### Install Dependencies

```bash
uv sync
```

### Database Setup

#### Option 1: Neon Serverless PostgreSQL (Recommended for Production)

1. Create a free account at [Neon](https://neon.tech)
2. Create a new project and database
3. Copy your connection string from the Neon dashboard
4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Edit `.env` with your Neon connection string:

```env
DATABASE_URL=postgresql://username:password@ep-xxx.region.neon.tech/dbname?sslmode=require
```

#### Option 2: SQLite (Local Development)

No configuration needed! The app defaults to SQLite if `DATABASE_URL` is not set.

### Run Tests

```bash
uv run pytest -v
uv run pytest --cov=app --cov-report=term-missing
```

### Run Server

```bash
uv run fastapi dev app/main.py
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | List all tasks |
| GET | `/tasks/{id}` | Get a specific task |
| PATCH | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example Requests

### Create Task
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high"}'
```

### List Tasks
```bash
curl http://localhost:8000/tasks/
```

### Get Task
```bash
curl http://localhost:8000/tasks/1
```

### Update Task
```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete Task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Task Model

```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the API implementation",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59",
  "created_at": "2025-01-08T10:00:00",
  "updated_at": "2025-01-08T10:00:00"
}
```

### Status Values
- `pending` (default)
- `in_progress`
- `completed`
- `cancelled`

### Priority Values
- `low`
- `medium` (default)
- `high`
- `urgent`

## Neon Database Benefits

- **Serverless**: Scales to zero when not in use
- **Branching**: Create database branches for dev/test
- **Free Tier**: Generous free plan for development
- **PostgreSQL**: Full PostgreSQL compatibility

## Development

Built following TDD (Test-Driven Development) practices:
1. Write failing tests first (RED)
2. Implement minimal code to pass (GREEN)
3. Refactor while keeping tests green (REFACTOR)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///database.db` |

## License

MIT
