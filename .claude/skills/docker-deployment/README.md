# Docker Deployment Skill

Containerize Python/FastAPI applications with Docker and UV package manager — from hello world to professional production deployments.

## Overview

This skill provides comprehensive guidance for containerizing FastAPI applications using modern best practices:

- **UV Package Manager** — 10-100x faster than pip
- **Multi-stage Builds** — Minimal production images
- **Security Hardening** — Non-root users, secrets management
- **Docker Compose** — Development and production stacks

## Quick Start

### 1. Invoke the Skill

```
/docker-deployment
```

### 2. Choose Your Deployment Level

| Level | Use Case | Command |
|-------|----------|---------|
| Hello World | Learning, demos | `docker build -t myapp . && docker run -p 8000:8000 myapp` |
| Development | Local dev with hot-reload | `docker compose -f compose.dev.yaml up --build` |
| Production | Staging/production | `docker compose -f compose.prod.yaml up -d` |
| Full Stack | Complete app with DB | Use production compose with PostgreSQL & Redis |

## Skill Structure

```
docker-deployment/
├── SKILL.md                    # Main skill with workflows & decision trees
├── references/
│   ├── production-dockerfile.md   # Production Dockerfile patterns
│   ├── compose-patterns.md        # Docker Compose configurations
│   ├── uv-docker.md               # UV-specific optimizations
│   └── security.md                # Security hardening guide
└── templates/
    ├── Dockerfile.dev             # Development Dockerfile
    ├── Dockerfile.prod            # Production Dockerfile
    ├── compose.dev.yaml           # Development compose
    ├── compose.prod.yaml          # Production compose
    ├── .dockerignore              # Docker ignore patterns
    └── pyproject.toml.example     # UV project template
```

## Features

### Deployment Levels

#### Level 1: Hello World
Minimal setup for learning Docker basics.

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev
COPY . .
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0"]
```

#### Level 2: Development
Hot-reload enabled for rapid development.

```bash
docker compose -f compose.dev.yaml up --build
```

Features:
- Volume mounts for live code changes
- Development dependencies included
- Debug mode enabled

#### Level 3: Production
Multi-stage build with security hardening.

```bash
docker compose -f compose.prod.yaml up -d
```

Features:
- Multi-stage build (smaller images)
- Non-root user
- Health checks
- Multiple workers

#### Level 4: Full Stack
Complete application stack with databases.

Features:
- PostgreSQL with health checks
- Redis for caching
- Docker secrets for passwords
- Network isolation

## Using Templates

Copy templates to your project:

```bash
# Copy production Dockerfile
cp .claude/skills/docker-deployment/templates/Dockerfile.prod ./Dockerfile

# Copy development setup
cp .claude/skills/docker-deployment/templates/Dockerfile.dev ./
cp .claude/skills/docker-deployment/templates/compose.dev.yaml ./

# Copy .dockerignore
cp .claude/skills/docker-deployment/templates/.dockerignore ./
```

## Prerequisites

Your project needs:

1. **pyproject.toml** — Project configuration
2. **uv.lock** — Dependency lockfile (run `uv lock`)
3. **Health endpoint** — Add `/health` route to your FastAPI app

```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## Common Commands

```bash
# Build image
docker build -t myapp .

# Run container
docker run -p 8000:8000 myapp

# Development with hot-reload
docker compose -f compose.dev.yaml up --build

# Production deployment
docker compose -f compose.prod.yaml up -d

# View logs
docker compose logs -f app

# Scale application
docker compose up -d --scale app=3

# Scan for vulnerabilities
docker scout cves myapp:latest
```

## Security Checklist

| Check | Implementation |
|-------|----------------|
| Non-root user | `USER app` in Dockerfile |
| Minimal base image | `python:3.12-slim-bookworm` |
| No secrets in image | Docker secrets or env vars |
| Health checks | `HEALTHCHECK` instruction |
| Resource limits | `--memory`, `--cpus` flags |
| Vulnerability scan | Docker Scout or Trivy |

## Knowledge Sources

This skill was built from official documentation:

- [Docker Official Docs](https://docs.docker.com/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [UV Docker Integration](https://docs.astral.sh/uv/guides/integration/docker/)
- [Astral UV Docker Example](https://github.com/astral-sh/uv-docker-example)

## What This Skill Does NOT Cover

- Kubernetes deployments
- CI/CD pipeline setup
- Cloud-specific services (AWS ECS, GCP Cloud Run)
- Windows containers

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `uv.lock` not found | Run `uv lock` before building |
| Permission denied | Check `USER` instruction and file ownership |
| Hot-reload not working | Ensure volume mount excludes `.venv` |
| Health check failing | Verify `/health` endpoint exists |
| Large image size | Use multi-stage build |

## License

Part of [Claude Code Skills Lab](https://github.com/anthropics/claude-code-skills-lab)