# FastAPI Development Skill

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-purple)](https://github.com/astral-sh/uv)

A comprehensive Claude Code skill for building modern, fast Python APIs - from hello world to production-ready applications.

## Overview

This skill provides Claude with deep knowledge of FastAPI development, enabling assistance with:

- **Project Setup** - Initialize projects with UV package manager
- **REST APIs** - Build complete CRUD operations
- **Data Validation** - Pydantic models and schemas
- **Database Integration** - SQLAlchemy with async support
- **Authentication** - JWT tokens and OAuth2 flows
- **Advanced Features** - WebSockets, background tasks, middleware
- **Testing** - pytest with async support and TDD workflows
- **Deployment** - Docker, production configurations

## Trigger Phrases

The skill activates when you mention:

- "create a FastAPI app"
- "build an API"
- "add authentication"
- "connect database"
- "deploy FastAPI"
- Any FastAPI-related development task

## Skill Structure

```
fastapi/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── references/
│   ├── basics.md         # Installation, routing, parameters
│   ├── models-validation.md  # Pydantic schemas
│   ├── database.md       # SQLAlchemy, async DB operations
│   ├── authentication.md # JWT, OAuth2, security
│   ├── advanced.md       # WebSockets, background tasks
│   ├── testing.md        # pytest, TDD workflow
│   └── deployment.md     # Docker, production setup
└── assets/
    └── starter-template/ # Ready-to-use project template
```

## Quick Start Example

When you ask Claude to create a FastAPI app, it uses this skill to provide:

```bash
uv init my-api && cd my-api
uv add "fastapi[standard]"
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

```bash
uv run fastapi dev main.py
```

Access at `http://127.0.0.1:8000` | Docs at `/docs`

## Topics Covered

### Basics
- Installation with UV
- Path & query parameters
- Request/response models
- Status codes
- Headers & cookies

### Data Validation
- Pydantic BaseModel
- Field validation
- Custom validators
- Nested models

### Database
- SQLAlchemy setup
- Async database operations
- Migrations with Alembic
- Repository pattern

### Authentication
- JWT token generation
- OAuth2 password flow
- Protected routes
- Role-based access

### Advanced
- Background tasks
- WebSocket connections
- Custom middleware
- CORS configuration
- File uploads

### Testing
- pytest setup
- Async test fixtures
- API endpoint testing
- TDD workflow

### Deployment
- Docker configuration
- Environment variables
- Production server setup
- Health checks

## Starter Template

The skill includes a production-ready starter template at `assets/starter-template/` with:

- Proper project structure
- Configuration management
- Health check endpoint
- Example router and schemas
- Environment file template

## Usage Tips

1. **Starting fresh?** Ask Claude to "create a new FastAPI project"
2. **Adding features?** Ask for specific features like "add JWT authentication"
3. **Need help?** Ask about any FastAPI concept - routing, models, dependencies, etc.
4. **Debugging?** Share your code and ask Claude to help troubleshoot

## Requirements

- Python 3.10+
- UV package manager (recommended)
- FastAPI with standard extras

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [UV Documentation](https://github.com/astral-sh/uv)

## License

This skill is part of the Claude Code Skills Lab.
