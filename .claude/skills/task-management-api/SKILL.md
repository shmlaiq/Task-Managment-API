---
name: task-management-api
description: Task Management REST API built with FastAPI, SQLModel, and UV using Test-Driven Development. This skill should be used when building task/todo APIs, learning TDD with FastAPI, or as a reference for SQLModel + FastAPI integration.
allowed-tools: Bash(uv:*), Bash(pytest:*), Bash(python:*), Read, Glob, Grep, Write, Edit
---

# Task Management API

A production-ready Task Management REST API built with **FastAPI + SQLModel + UV** using **Test-Driven Development (TDD)**.

## Before Implementation

Gather context before building or extending this API:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models in `app/models/`, router patterns, test fixtures |
| **Conversation** | New features needed, custom fields, filtering requirements |
| **Assets** | Reference implementation in `assets/task-management-api/` |
| **User Guidelines** | Database preference (Neon/SQLite), deployment target |

## Clarifications

### Required (ask if extending)
1. **New entity?** Tasks only / Add users / Add categories
2. **Database?** Neon PostgreSQL / SQLite (local dev)
3. **Authentication?** JWT / API Key / None

### Optional
4. **Additional fields?** Tags / Attachments / Comments
5. **Filtering needs?** By status / By priority / By date range

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| FastAPI Docs | https://fastapi.tiangolo.com | API patterns |
| SQLModel Docs | https://sqlmodel.tiangolo.com | ORM models |
| Neon Docs | https://neon.tech/docs | Serverless PostgreSQL |
| Pytest Docs | https://docs.pytest.org | Testing |

> **Version Note**: Built with FastAPI 0.100+, SQLModel 0.0.16+, Python 3.12+.

## Features

- Full CRUD operations (Create, Read, Update, Delete)
- Task priority levels (low, medium, high, urgent)
- Task status tracking (pending, in_progress, completed, cancelled)
- Due date management
- Filtering and pagination
- **Neon Serverless PostgreSQL** support (with SQLite fallback)
- SQLModel ORM for database operations
- Comprehensive test suite with pytest
- UV package manager for fast dependency management

## Quick Start

### Installation

```bash
cd task-management-api
uv sync
```

### Database Setup (Neon)

1. Create account at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy connection string and create `.env`:

```bash
cp .env.example .env
# Edit .env with your Neon connection string:
# DATABASE_URL=postgresql://user:pass@ep-xxx.region.neon.tech/dbname?sslmode=require
```

Without `.env`, the app uses SQLite for local development.

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

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
task-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel models
│   └── routers/
│       ├── __init__.py
│       └── tasks.py         # Task CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   └── test_tasks.py        # Task API tests
├── pyproject.toml
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | List all tasks (with pagination) |
| GET | `/tasks/{id}` | Get a specific task |
| PATCH | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/health` | Health check |

## Task Model

```python
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## TDD Workflow

This project follows strict TDD practices:

### 1. RED Phase - Write Failing Test
```python
def test_create_task(client):
    response = client.post("/tasks/", json={
        "title": "Complete project",
        "priority": "high"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Complete project"
```

### 2. GREEN Phase - Implement Minimal Code
```python
@router.post("/", response_model=TaskRead, status_code=201)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### 3. REFACTOR Phase - Improve Code Quality
Add validation, error handling, indexes while keeping tests green.

## Example Requests

### Create Task
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high", "status": "pending"}'
```

### List Tasks
```bash
curl http://localhost:8000/tasks/
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

## References

- [TDD Guide](../pytest/references/tdd.md) - Test-Driven Development practices
- [FastAPI Integration](../sqlmodel/references/fastapi-integration.md) - SQLModel + FastAPI patterns
- [Testing Patterns](../pytest/references/fastapi_testing.md) - FastAPI testing best practices

## Development

### Run Specific Test
```bash
uv run pytest tests/test_tasks.py::test_create_task -v
```

### Watch Mode (Continuous TDD)
```bash
uv add pytest-watch --dev
uv run ptw -- -v
```

### Coverage Report
```bash
uv run pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Missing `.env` file | Database connection fails | Copy `.env.example` to `.env` |
| Not running migrations | Tables don't exist | Tables auto-create on startup |
| Wrong status code for POST | Should be 201, not 200 | Use `status_code=201` |
| Missing 404 handling | Returns 500 on not found | Check `session.get()` result |
| Forgetting `session.refresh()` | Response missing DB-generated fields | Refresh after commit |
| Tests affecting each other | Flaky tests | Use fresh DB per test |

## Before Delivery Checklist

### API Quality
- [ ] All CRUD endpoints working
- [ ] Proper HTTP status codes (201, 204, 404)
- [ ] Input validation via Pydantic
- [ ] Error responses are consistent

### Database
- [ ] `.env` configured for target database
- [ ] Models have proper indexes
- [ ] Timestamps auto-generated

### Testing
- [ ] All tests pass: `uv run pytest -v`
- [ ] Coverage acceptable: `uv run pytest --cov=app`
- [ ] TDD followed (tests written first)

### Documentation
- [ ] Swagger UI accessible at `/docs`
- [ ] Endpoints have proper tags
- [ ] Request/response examples visible
