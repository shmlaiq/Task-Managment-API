# Task Managment API

A production-ready **Task Management REST API** built with modern Python stack using **Test-Driven Development (TDD)**.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.22+-orange.svg)
![Neon](https://img.shields.io/badge/Neon-PostgreSQL-00E599.svg)
![Tests](https://img.shields.io/badge/Tests-29%20passed-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg)

## Features

- Full **CRUD operations** (Create, Read, Update, Delete)
- Task **priority levels** (low, medium, high, urgent)
- Task **status tracking** (pending, in_progress, completed, cancelled)
- **Due date** management
- **Pagination** support
- **Neon Serverless PostgreSQL** (with SQLite fallback for local dev)
- **29 comprehensive tests** with pytest
- **95% code coverage**
- Built with **TDD** (Test-Driven Development)

## Tech Stack

| Technology | Purpose |
|------------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Modern async web framework |
| [SQLModel](https://sqlmodel.tiangolo.com/) | SQL database ORM (Pydantic + SQLAlchemy) |
| [Neon](https://neon.tech/) | Serverless PostgreSQL database |
| [UV](https://github.com/astral-sh/uv) | Fast Python package manager |
| [pytest](https://pytest.org/) | Testing framework |


## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/shmlaiq/Task-Managment-API.git
cd Task-Managment-API/.claude/skills/task-management-api/assets/task-management-api
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Database Setup

#### Option A: Neon PostgreSQL (Recommended)

1. Create a free account at [neon.tech](https://neon.tech)
2. Create a new project and database
3. Copy your connection string
4. Create `.env` file:

```bash
cp .env.example .env
```

5. Add your Neon connection string:

```env
DATABASE_URL=postgresql://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require
```

#### Option B: SQLite (Local Development)

No configuration needed! The app defaults to SQLite if `DATABASE_URL` is not set.

### 4. Run the Server

```bash
uv run uvicorn app.main:app --reload
```

### 5. Access API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc


### 6. Task Managment API Vedio
#### [Watch Screen Recording #1](https://onedrive.live.com/?redeem=aHR0cHM6Ly8xZHJ2Lm1zL2YvYy82MTQyOThkOTE0MGNiZWZjL0lnQnd2SlBIM0FvS1I1MjUxaFJ2M2pvU0FlN0U4eTBkWFBOSDQtUEZmWU52Yk00P2U9MzZLajZn&cid=614298D9140CBEFC&id=614298D9140CBEFC%21s00a325ce5be44ede94a23dc9c9473ea6&parId=614298D9140CBEFC%21sfe71bc07ffd5472f9260421fe81daaf3&o=OneUp)
######          Or
#### [Watch Screen Recording #2](https://www.youtube.com/watch?v=HNDgBKQOtO4)



## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |
| `POST` | `/tasks/` | Create a new task |
| `GET` | `/tasks/` | List all tasks (with pagination) |
| `GET` | `/tasks/{id}` | Get a specific task |
| `PATCH` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

## Example Usage

### Create a Task

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high"}'
```

**Response:**
```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": null,
  "status": "pending",
  "priority": "high",
  "due_date": null,
  "created_at": "2026-01-08T18:00:00",
  "updated_at": "2026-01-08T18:00:00"
}
```

### List Tasks

```bash
curl http://localhost:8000/tasks/
```

### Update a Task

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a Task

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
  "created_at": "2026-01-08T10:00:00",
  "updated_at": "2026-01-08T10:00:00"
}
```

### Status Values
| Status | Description |
|--------|-------------|
| `pending` | Task not started (default) |
| `in_progress` | Task is being worked on |
| `completed` | Task is finished |
| `cancelled` | Task was cancelled |

### Priority Values
| Priority | Description |
|----------|-------------|
| `low` | Low priority |
| `medium` | Normal priority (default) |
| `high` | High priority |
| `urgent` | Urgent priority |

## Running Tests

```bash
# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=app --cov-report=term-missing

# Run specific test
uv run pytest tests/test_tasks.py::TestCreateTask -v
```

### Test Results

```
29 passed in 1.16s
Coverage: 95%
```

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
│   └── test_tasks.py        # Task API tests (29 tests)
├── .env.example             # Environment template
├── .gitignore
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Locked dependencies
└── README.md
```

## Development Approach

This project was built using **Test-Driven Development (TDD)**:

1. **RED** - Write failing tests first
2. **GREEN** - Write minimal code to pass tests
3. **REFACTOR** - Improve code while keeping tests green

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///database.db` |

## Why Neon?

- **Serverless**: Scales to zero when not in use
- **Branching**: Git-like database branching for dev/test
- **Free Tier**: Generous free plan for development
- **PostgreSQL**: Full PostgreSQL compatibility

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to use this project for learning or production!

## Author

**Muhammad Faisal Laiq**
- GitHub: [@shmlaiq](https://github.com/shmlaiq)
- Email: shmlaiq@gmail.com

---

Built with using  =>   FastAPI, SQLModel, and Neon PostgreSQL
