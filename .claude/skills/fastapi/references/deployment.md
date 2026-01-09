# Production Deployment

## Table of Contents
- [Configuration](#configuration)
- [Docker](#docker)
- [Gunicorn + Uvicorn](#gunicorn--uvicorn)
- [Cloud Platforms](#cloud-platforms)
- [Nginx Reverse Proxy](#nginx-reverse-proxy)
- [Health Checks & Monitoring](#health-checks--monitoring)
- [Production Checklist](#production-checklist)

## Configuration

### Environment-Based Settings

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "My API"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list[str] = ["https://yourdomain.com"]

    # External Services
    REDIS_URL: str | None = None
    SENTRY_DSN: str | None = None

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Environment Files

```bash
# .env.example (commit this)
APP_NAME=My API
DEBUG=false
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=your-secret-key-here

# .env (never commit - add to .gitignore)
```

## Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application
COPY ./app ./app

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-Stage Build (Smaller Image)

```dockerfile
# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy uv and virtual environment
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=builder /app/.venv /app/.venv

# Copy application
COPY ./app ./app

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    expose:
      - 8000
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - api
    restart: unless-stopped
```

## Gunicorn + Uvicorn

### Installation
```bash
uv add gunicorn "uvicorn[standard]"
```

### Configuration

```python
# gunicorn.conf.py
import multiprocessing

# Bind
bind = "0.0.0.0:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Timeouts
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "fastapi-app"

# Graceful restart
graceful_timeout = 30
```

### Running
```bash
# With config file
uv run gunicorn app.main:app -c gunicorn.conf.py

# Inline
uv run gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

## Cloud Platforms

### Railway

```toml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: fastapi-app
    env: docker
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: mydb
          property: connectionString
```

### Fly.io

```toml
# fly.toml
app = "my-fastapi-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true

  [[http_service.checks]]
    interval = "10s"
    timeout = "2s"
    path = "/health"

[env]
  ENVIRONMENT = "production"
```

```bash
fly launch
fly secrets set SECRET_KEY=your-secret DATABASE_URL=your-db-url
fly deploy
```

### AWS (ECS/Fargate)

```json
// task-definition.json
{
  "family": "fastapi-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-ecr-repo/fastapi-app:latest",
      "portMappings": [
        {"containerPort": 8000, "protocol": "tcp"}
      ],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"}
      ],
      "secrets": [
        {"name": "DATABASE_URL", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

## Nginx Reverse Proxy

```nginx
# nginx.conf
upstream api {
    server api:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /static/ {
        alias /app/static/;
        expires 30d;
    }
}
```

## Health Checks & Monitoring

### Health Endpoints

```python
# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "not ready", "database": str(e)}

@router.get("/health/live")
async def liveness():
    return {"status": "alive"}
```

### Logging

```python
# app/core/logging.py
import logging
import sys
from app.core.config import settings

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Silence noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# Structured logging with structlog
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()
logger.info("request_processed", user_id=123, endpoint="/users")
```

### Sentry Integration

```python
# app/main.py
import sentry_sdk
from app.core.config import settings

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1,
    )
```

## Production Checklist

### Security
- [ ] Use HTTPS everywhere
- [ ] Set secure SECRET_KEY (min 32 chars, random)
- [ ] Enable CORS with specific origins (not `*`)
- [ ] Use environment variables for secrets
- [ ] Add rate limiting
- [ ] Validate all inputs
- [ ] Use parameterized queries (SQLAlchemy handles this)
- [ ] Set security headers (via Nginx or middleware)

### Performance
- [ ] Use async database driver (asyncpg, aiosqlite)
- [ ] Add database connection pooling
- [ ] Enable response compression
- [ ] Add caching (Redis) for expensive operations
- [ ] Use CDN for static files
- [ ] Optimize database queries (indexes, eager loading)

### Reliability
- [ ] Add health check endpoints
- [ ] Configure graceful shutdown
- [ ] Set up monitoring and alerting
- [ ] Implement structured logging
- [ ] Add error tracking (Sentry)
- [ ] Configure auto-scaling

### Operations
- [ ] Use database migrations (Alembic)
- [ ] Set up CI/CD pipeline
- [ ] Create staging environment
- [ ] Document API (OpenAPI is automatic)
- [ ] Set up backups
- [ ] Create runbooks for common issues
