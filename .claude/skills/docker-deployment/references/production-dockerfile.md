# Production Dockerfile Reference

Complete, production-ready Dockerfile templates with UV package manager.

## Standard Production Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# ============================================================
# Production Dockerfile for FastAPI + UV
# Multi-stage build with security hardening
# ============================================================

# ==================== Builder Stage ====================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Compile bytecode for faster startup
ENV UV_COMPILE_BYTECODE=1
# Copy mode for Docker (not symlinks)
ENV UV_LINK_MODE=copy
# Use system Python (same version in both stages)
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies BEFORE copying source (better layer caching)
# Dependencies change less frequently than source code
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Now copy source and install the project itself
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ==================== Production Stage ====================
FROM python:3.12-slim-bookworm AS production

# Security: Create non-root user
# --no-create-home: No home directory needed
# --shell /sbin/nologin: Cannot login interactively
RUN groupadd --system --gid 1000 app \
    && useradd --system --gid 1000 --uid 1000 \
       --no-create-home --shell /sbin/nologin app

WORKDIR /app

# Copy application from builder (with proper ownership)
COPY --from=builder --chown=app:app /app /app

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"
# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Unbuffered output (important for logging)
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER app

# Document the port (doesn't publish it)
EXPOSE 8000

# Health check using Python (no curl needed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

# Run with multiple workers for production
# Adjust workers based on CPU: (2 * cores) + 1
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Standalone Dockerfile (Managed Python)

For complete Python version control without system Python:

```dockerfile
# syntax=docker/dockerfile:1
# Uses UV-managed Python for complete control over Python version

# ==================== Builder Stage ====================
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
# Directory for UV-managed Python
ENV UV_PYTHON_INSTALL_DIR=/python
# Only use UV-managed Python, no system Python
ENV UV_PYTHON_PREFERENCE=only-managed

# Install specific Python version
RUN uv python install 3.12

WORKDIR /app

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ==================== Production Stage ====================
FROM debian:bookworm-slim AS production

# Non-root user
RUN groupadd --system --gid 1000 app \
    && useradd --system --gid 1000 --uid 1000 --create-home app

# Copy UV-managed Python
COPY --from=builder --chown=app:app /python /python
# Copy application
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER app
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Alpine-based Dockerfile (Smaller Image)

For minimal image size (note: some packages may need compilation):

```dockerfile
# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM python:3.12-alpine AS production

RUN addgroup -g 1000 -S app \
    && adduser -S -G app -u 1000 app

WORKDIR /app
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Layer Caching Strategy

Order Dockerfile instructions by change frequency:

```
Most stable (top)     → Base image, system packages
                      → UV installation
                      → pyproject.toml, uv.lock (dependencies)
Most volatile (bottom)→ Application source code
```

This ensures that changing source code doesn't invalidate dependency layers.

## Build Arguments for Flexibility

```dockerfile
ARG PYTHON_VERSION=3.12
ARG UV_VERSION=latest
ARG WORKERS=4

FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder
# ...

FROM python:${PYTHON_VERSION}-slim-bookworm AS production
# ...
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "${WORKERS}"]
```

Build with custom args:
```bash
docker build --build-arg PYTHON_VERSION=3.11 --build-arg WORKERS=8 -t myapp .
```

## Image Size Comparison

| Base Image | Approximate Size |
|------------|------------------|
| python:3.12 | ~1GB |
| python:3.12-slim | ~150MB |
| python:3.12-slim-bookworm | ~130MB |
| python:3.12-alpine | ~50MB |
| debian:bookworm-slim + UV Python | ~100MB |

Multi-stage builds significantly reduce final image size by excluding build tools.
