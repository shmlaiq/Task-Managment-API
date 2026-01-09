# SQLModel Skill

[![Claude Code](https://img.shields.io/badge/Claude-Code-7C3AED?logo=anthropic&logoColor=white)](https://claude.ai/claude-code)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.22-009485?logo=pydantic&logoColor=white)](https://sqlmodel.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Compatible-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Claude Code skill for building database applications with **SQLModel** - the library that combines Pydantic and SQLAlchemy into one elegant solution.

## Overview

SQLModel is created by Sebastián Ramírez (the creator of FastAPI) and provides:

- **One model** for both validation AND database
- **Type hints** everywhere for excellent IDE support
- **Pydantic** compatibility for data validation
- **SQLAlchemy** power for database operations
- **FastAPI** integration out of the box

## When to Use This Skill

This skill triggers automatically when you:

- Ask to "create database model"
- Ask to "add SQLModel"
- Work on "database with FastAPI"
- Need "ORM model" functionality
- Any SQLModel-related development

## Features

| Feature | Description |
|---------|-------------|
| TDD Workflow | Red-Green-Refactor approach for reliable code |
| Model Inheritance | Base, Create, Read, Update schemas |
| CRUD Operations | Complete Create, Read, Update, Delete patterns |
| FastAPI Integration | Dependency injection, async support |
| Relationships | One-to-Many, Many-to-Many patterns |
| Migrations | Alembic integration for schema changes |
| Async Support | asyncpg, aiosqlite for async operations |
| Testing | pytest fixtures with in-memory database |

## Quick Start

```bash
# Initialize project
uv init my-app && cd my-app

# Install SQLModel
uv add sqlmodel

# For FastAPI integration
uv add sqlmodel fastapi "uvicorn[standard]"

# For async PostgreSQL
uv add sqlmodel asyncpg
```

## Basic Example

```python
from sqlmodel import Field, SQLModel, Session, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

# Create engine and tables
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# CRUD operations
with Session(engine) as session:
    # Create
    hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    session.add(hero)
    session.commit()

    # Read
    heroes = session.exec(select(Hero)).all()
```

## Project Structure

```
sqlmodel/
├── SKILL.md              # Main skill instructions
├── README.md             # This file
└── references/
    ├── basics.md         # SQLModel fundamentals
    ├── fastapi-integration.md  # FastAPI + SQLModel
    ├── relationships.md  # 1:N, N:N relationships
    ├── migrations.md     # Alembic migrations
    └── async.md          # Async database operations
```

## Reference Guides

| Guide | Description |
|-------|-------------|
| [basics.md](references/basics.md) | SQLModel fundamentals and core concepts |
| [fastapi-integration.md](references/fastapi-integration.md) | Building FastAPI apps with SQLModel |
| [relationships.md](references/relationships.md) | One-to-Many, Many-to-Many relationships |
| [migrations.md](references/migrations.md) | Database migrations with Alembic |
| [async.md](references/async.md) | Async database operations |

## TDD Workflow

This skill emphasizes **Test-Driven Development**:

```
🔴 RED    → Write a failing test for model/endpoint
🟢 GREEN  → Create minimal model/code to pass
🔄 REFACTOR → Improve code, keep tests green
```

### Example TDD Cycle

```python
# Step 1: 🔴 RED - Write test first
def test_create_hero(client):
    response = client.post("/heroes/", json={
        "name": "Spider-Boy",
        "secret_name": "Pedro Parqueador"
    })
    assert response.status_code == 201

# Step 2: 🟢 GREEN - Create model to pass test
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str

# Step 3: 🔄 REFACTOR - Add indexes, validation
```

## Testing Setup

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",  # In-memory database
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```

```bash
# Run tests
uv run pytest tests/ -v
uv run pytest tests/ --cov=app --cov-report=term-missing
```

## Database Support

| Database | Sync Driver | Async Driver |
|----------|-------------|--------------|
| SQLite | Built-in | `aiosqlite` |
| PostgreSQL | `psycopg2` | `asyncpg` |
| MySQL | `pymysql` | `aiomysql` |

## Related Skills

- **[fastapi](../fastapi/)** - Comprehensive FastAPI development
- **[fastapi-builder](../fastapi-builder/)** - Generate FastAPI projects
- **[pytest](../pytest/)** - Python testing with pytest

## Resources

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [SQLModel GitHub](https://github.com/tiangolo/sqlmodel)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

MIT License - See [LICENSE](LICENSE) for details.

---

*Generated with [Claude Code](https://claude.ai/claude-code)*
