# Docker Security Hardening

Security best practices for production Docker deployments.

## Non-Root User

**Always run containers as non-root.**

### Creating Non-Root User (Debian/Ubuntu)
```dockerfile
# Create group and user with specific UID/GID
RUN groupadd --system --gid 1000 app \
    && useradd --system --gid 1000 --uid 1000 \
       --no-create-home --shell /sbin/nologin app

# Set ownership
COPY --chown=app:app . /app

# Switch to non-root
USER app
```

### Creating Non-Root User (Alpine)
```dockerfile
RUN addgroup -g 1000 -S app \
    && adduser -S -G app -u 1000 app

USER app
```

### Why Specific UID/GID?
- Deterministic across rebuilds
- Consistent permissions with host volumes
- Easier debugging and auditing

## Minimal Base Images

| Image | Size | Security |
|-------|------|----------|
| `python:3.12` | ~1GB | Many packages, larger attack surface |
| `python:3.12-slim` | ~150MB | Reduced packages |
| `python:3.12-slim-bookworm` | ~130MB | Recommended for production |
| `python:3.12-alpine` | ~50MB | Smallest, but musl libc issues |
| `distroless` | ~20MB | No shell, most secure |

### Distroless Example
```dockerfile
FROM python:3.12-slim AS builder
# ... build stage ...

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /app /app
CMD ["app/main.py"]
```

## Multi-Stage Builds

Separate build and runtime to exclude build tools:

```dockerfile
# Build stage has all build dependencies
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y build-essential
# ... build ...

# Production stage is minimal
FROM python:3.12-slim AS production
# Only copy runtime artifacts, not build tools
COPY --from=builder /app /app
```

## No Secrets in Images

### Bad: Secrets in Image
```dockerfile
# NEVER do this
ENV API_KEY=secret123
COPY .env /app/.env
```

### Good: Runtime Secrets

#### Environment Variables
```yaml
# compose.yaml
services:
  app:
    environment:
      - API_KEY=${API_KEY}  # From host environment
```

#### Docker Secrets
```yaml
secrets:
  api_key:
    file: ./secrets/api_key.txt

services:
  app:
    secrets:
      - api_key
    environment:
      - API_KEY_FILE=/run/secrets/api_key
```

#### Read Secret in Python
```python
import os
from pathlib import Path

def get_secret(name: str) -> str:
    """Read secret from file or environment."""
    file_path = os.getenv(f"{name}_FILE")
    if file_path:
        return Path(file_path).read_text().strip()
    return os.getenv(name, "")

db_password = get_secret("DB_PASSWORD")
```

## Read-Only Filesystem

Run containers with read-only root filesystem:

```bash
docker run --read-only --tmpfs /tmp myapp
```

```yaml
# compose.yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
    volumes:
      - app_data:/app/data  # Writable volume for data
```

## Resource Limits

Prevent resource exhaustion attacks:

```bash
docker run \
  --memory=512m \
  --memory-swap=512m \
  --cpus=1 \
  --pids-limit=100 \
  myapp
```

```yaml
# compose.yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
```

## Health Checks

Detect compromised or stuck containers:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
```

## Network Security

### Internal Networks
```yaml
networks:
  backend:
    internal: true  # No external access

services:
  db:
    networks:
      - backend  # Only accessible internally
```

### Limit Exposed Ports
```yaml
services:
  app:
    expose:
      - "8000"  # Internal only

  nginx:
    ports:
      - "80:80"  # Only nginx exposed
```

## Vulnerability Scanning

### Docker Scout
```bash
# Scan for vulnerabilities
docker scout cves myapp:latest

# Quick overview
docker scout quickview myapp:latest

# Recommendations
docker scout recommendations myapp:latest
```

### Trivy
```bash
trivy image myapp:latest
```

### GitHub Actions Integration
```yaml
- name: Run Docker Scout
  uses: docker/scout-action@v1
  with:
    command: cves
    image: myapp:latest
    only-severities: critical,high
    exit-code: true  # Fail on vulnerabilities
```

## Security Checklist

| Check | Implementation |
|-------|----------------|
| Non-root user | `USER app` in Dockerfile |
| Minimal base | `python:3.12-slim-bookworm` |
| Multi-stage build | Separate builder and production stages |
| No secrets in image | Use env vars or Docker secrets |
| Read-only filesystem | `--read-only` flag |
| Resource limits | `--memory`, `--cpus` |
| Health checks | `HEALTHCHECK` instruction |
| Vulnerability scan | Docker Scout or Trivy |
| Network isolation | Internal networks for databases |
| Updated base images | Regular rebuilds with `--pull` |

## Production Dockerfile Security

```dockerfile
# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM python:3.12-slim-bookworm AS production

# Security hardening
RUN groupadd --system --gid 1000 app \
    && useradd --system --gid 1000 --uid 1000 \
       --no-create-home --shell /sbin/nologin app \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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

## Runtime Security Flags

```bash
docker run \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  --user 1000:1000 \
  myapp
```

| Flag | Purpose |
|------|---------|
| `--read-only` | Read-only root filesystem |
| `--tmpfs /tmp` | Writable tmp in memory |
| `--no-new-privileges` | Prevent privilege escalation |
| `--cap-drop=ALL` | Drop all Linux capabilities |
| `--user` | Run as specific UID/GID |
