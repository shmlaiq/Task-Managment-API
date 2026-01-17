---
name: docker-deployment
description: |
  Containerize Python/FastAPI applications with Docker and UV package manager.
  This skill should be used when users want to create Dockerfiles, docker-compose
  configurations, or deploy FastAPI applications from hello world to production.
  Covers development hot-reload, multi-stage production builds, security hardening,
  health checks, and CI/CD patterns.
---

# Docker Deployment for Python/FastAPI with UV

Containerize Python/FastAPI applications from hello world to professional production deployments using UV package manager.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Check for existing Dockerfile, compose.yaml, pyproject.toml, requirements.txt |
| **Conversation** | Deployment target (dev/staging/prod), database needs, scaling requirements |
| **Skill References** | Templates in `references/`, Dockerfile patterns, compose patterns |

## Required Clarifications

Ask these before implementation:

### Required
1. **Deployment target** - "Is this for development, staging, or production?"
2. **Project setup** - "Do you have `pyproject.toml` and `uv.lock`, or should I create them?"

### Optional (ask if relevant)
3. **Database needs** - "Do you need PostgreSQL, Redis, or other services?"
4. **Scaling** - "Single instance or multiple replicas behind a load balancer?"
5. **Reverse proxy** - "Need nginx or traefik for SSL/routing?"

> If user doesn't specify, default to **Development** setup with option to upgrade later.

## Quick Start Decision Tree

```
What do you need?
│
├─ Just learning/hello world → Use "Hello World" section
├─ Local development → Use "Development Setup"
├─ Production deployment → Use "Production Build"
└─ Full stack with DB → Use "Docker Compose"
```

## Deployment Levels

| Level | Use Case | Key Features |
|-------|----------|--------------|
| **Hello World** | Learning, demos | Single Dockerfile, minimal config |
| **Development** | Local dev work | Hot-reload, volume mounts, dev dependencies |
| **Production** | Staging/prod | Multi-stage, non-root user, health checks |
| **Full Stack** | Complete apps | Compose with DB, Redis, networking, secrets |

---

## Level 1: Hello World

Minimal Dockerfile for learning and quick demos.

### Dockerfile (Hello World)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Copy application
COPY . .

# Run FastAPI
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run

```bash
docker build -t myapp .
docker run -p 8000:8000 myapp
```

---

## Level 2: Development Setup

Development environment with hot-reload and mounted volumes.

### Dockerfile.dev

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Environment setup
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Non-root user for security
RUN groupadd --system --gid 1000 app \
    && useradd --system --gid 1000 --uid 1000 --create-home app

# Install dependencies (cached layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked

# Copy application
COPY --chown=app:app . .

USER app

# Hot-reload enabled for development
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
```

### compose.dev.yaml

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - .:/app  # Mount source for hot-reload
      - /app/.venv  # Exclude venv from mount
    environment:
      - DEBUG=true
```

### Run Development

```bash
docker compose -f compose.dev.yaml up --build
```

---

## Level 3: Production Build

Multi-stage build with security hardening. See `references/production-dockerfile.md` for complete template.

### Dockerfile (Production)

```dockerfile
# ============ Builder Stage ============
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first (better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy source and sync project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ============ Production Stage ============
FROM python:3.12-slim-bookworm

# Security: non-root user
RUN groupadd --system --gid 1000 app \
    && useradd --system --gid 1000 --uid 1000 \
       --no-create-home --shell /sbin/nologin app

WORKDIR /app

# Copy only runtime artifacts
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER app

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Production Build Commands

```bash
# Build with cache
docker build -t myapp:prod --target production .

# Run with resource limits
docker run -d \
  --name myapp \
  -p 8000:8000 \
  --memory=512m \
  --cpus=1 \
  --restart=unless-stopped \
  myapp:prod
```

---

## Level 4: Full Stack with Docker Compose

Complete stack with PostgreSQL, Redis, and production configuration.

### compose.yaml (Production Stack)

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/appdb
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Stack Commands

```bash
# Create secrets directory
mkdir -p secrets
echo "your-secure-password" > secrets/db_password.txt

# Start stack
docker compose up -d

# View logs
docker compose logs -f app

# Scale app
docker compose up -d --scale app=3
```

---

## Essential Files

### .dockerignore

```
.git
.gitignore
.venv
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache
.coverage
htmlcov
.env
.env.*
!.env.example
*.md
!README.md
Dockerfile*
compose*.yaml
docker-compose*.yaml
```

### pyproject.toml (Minimal)

```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi[standard]>=0.115.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "httpx>=0.27",
]
```

### Health Endpoint

Add to your FastAPI app:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## Security Checklist

| Check | Implementation |
|-------|----------------|
| Non-root user | `USER app` in Dockerfile |
| Minimal base image | `python:3.12-slim-bookworm` |
| No secrets in image | Use Docker secrets or env vars |
| Read-only filesystem | `--read-only` flag or compose `read_only: true` |
| Health checks | HEALTHCHECK instruction |
| Resource limits | `--memory`, `--cpus` flags |
| Scan for CVEs | `docker scout cves myapp:prod` |

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `uv.lock` not found | Run `uv lock` before building |
| Permission denied | Check USER instruction and file ownership |
| Hot-reload not working | Ensure volume mount excludes `.venv` |
| Health check failing | Verify `/health` endpoint exists |
| Large image size | Use multi-stage build |
| Slow builds | Order layers by change frequency |

---

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| Docker Docs | https://docs.docker.com/ | Dockerfile reference, compose spec |
| FastAPI Deployment | https://fastapi.tiangolo.com/deployment/docker/ | FastAPI-specific patterns |
| UV Docker Guide | https://docs.astral.sh/uv/guides/integration/docker/ | UV Docker integration |
| UV Docker Example | https://github.com/astral-sh/uv-docker-example | Official UV Docker examples |
| Docker Best Practices | https://docs.docker.com/build/building/best-practices/ | Image optimization |

> **Version Note**: Docker, FastAPI, and UV evolve rapidly. For patterns not covered here or when troubleshooting, verify against official docs above for the latest best practices.

---

## Reference Files

| File | Content |
|------|---------|
| `references/production-dockerfile.md` | Complete production Dockerfile with comments |
| `references/compose-patterns.md` | Docker Compose patterns for various architectures |
| `references/uv-docker.md` | UV-specific Docker optimization techniques |
| `references/security.md` | Security hardening guide |
| `templates/` | Ready-to-use Dockerfile and compose templates |

### Advanced Patterns (Fetch from Official Docs)

For patterns not covered in this skill:
- **Multi-platform builds** → `docker buildx` documentation
- **BuildKit features** → Docker BuildKit docs
- **Compose profiles** → Docker Compose profiles spec
- **UV workspaces** → UV workspace documentation

---

## What This Skill Does NOT Cover

- Kubernetes deployments (use dedicated k8s skill)
- CI/CD pipeline setup (use ci-cd skill)
- Cloud-specific deployments (AWS ECS, GCP Cloud Run)
- Windows containers
