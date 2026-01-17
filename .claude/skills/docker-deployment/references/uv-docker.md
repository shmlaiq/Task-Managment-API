# UV Docker Integration

Optimizing Python Docker builds with UV package manager.

## UV Base Images

| Image | Use Case |
|-------|----------|
| `ghcr.io/astral-sh/uv:latest` | UV binary only (copy into other images) |
| `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` | Python + UV (recommended) |
| `ghcr.io/astral-sh/uv:python3.12-alpine` | Minimal size |
| `ghcr.io/astral-sh/uv:bookworm-slim` | UV with managed Python |

## Installing UV in Existing Images

### Copy Binary Method (Recommended)
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

### Pip Install Method (Alternative)
```dockerfile
FROM python:3.12-slim
RUN pip install uv
```

## Essential UV Environment Variables

```dockerfile
# Compile Python to bytecode for faster startup
ENV UV_COMPILE_BYTECODE=1

# Copy dependencies instead of symlinks (required for Docker)
ENV UV_LINK_MODE=copy

# Don't download Python (use system Python)
ENV UV_PYTHON_DOWNLOADS=0

# Tool binaries location
ENV UV_TOOL_BIN_DIR=/usr/local/bin
```

## Layer Caching Strategy

### Optimal Layer Order

```dockerfile
# 1. Base image (rarely changes)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# 2. Environment variables (rarely changes)
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 3. Working directory
WORKDIR /app

# 4. Dependencies ONLY (changes occasionally)
# Use bind mounts - files aren't copied into layer
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# 5. Source code (changes frequently)
COPY . /app

# 6. Install project (uses cached dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev
```

### Cache Mount Benefits

```dockerfile
# Cache mount persists UV's download cache between builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

- First build: Downloads all packages
- Subsequent builds: Uses cached packages
- Only downloads changed/new packages

## UV Sync Options

| Option | Purpose |
|--------|---------|
| `--locked` | Assert lockfile is up-to-date (fails if not) |
| `--frozen` | Don't update lockfile |
| `--no-dev` | Skip development dependencies |
| `--no-install-project` | Install deps only, not the project |
| `--no-install-workspace` | Skip workspace members |

### Production Build
```dockerfile
# Install dependencies without dev deps, don't install project yet
RUN uv sync --locked --no-install-project --no-dev

# Copy source
COPY . /app

# Now install the project (uses cached deps)
RUN uv sync --locked --no-dev
```

### Development Build
```dockerfile
# Include dev dependencies
RUN uv sync --locked
```

## Running Applications

### Using `uv run`
```dockerfile
# Runs command in the project's virtual environment
CMD ["uv", "run", "fastapi", "run", "--host", "0.0.0.0"]
```

### Direct Execution (Multi-stage)
```dockerfile
# In production stage, venv is in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run directly without uv
CMD ["fastapi", "run", "--host", "0.0.0.0"]
```

## Managed Python (Standalone)

For complete Python version control:

```dockerfile
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

# Store managed Python in known location
ENV UV_PYTHON_INSTALL_DIR=/python
# Only use UV-managed Python
ENV UV_PYTHON_PREFERENCE=only-managed

# Install specific Python version
RUN uv python install 3.12

# ... rest of build ...

FROM debian:bookworm-slim AS production
# Copy the managed Python
COPY --from=builder /python /python
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
```

## Project Structure Requirements

### Required Files
```
project/
├── pyproject.toml    # Project configuration
├── uv.lock           # Lockfile (commit this!)
├── src/              # Source code
│   └── myapp/
│       ├── __init__.py
│       └── main.py
└── .dockerignore     # Exclude unnecessary files
```

### .dockerignore for UV Projects
```
.git
.gitignore
.venv
__pycache__
*.pyc
.pytest_cache
.mypy_cache
.coverage
*.md
Dockerfile*
compose*.yaml
.env
.env.*
!.env.example
```

## Common UV Docker Issues

### Issue: `uv.lock` not found
```bash
# Generate lockfile before building
uv lock
```

### Issue: Stale lockfile
```dockerfile
# Use --locked to fail if lockfile is outdated
RUN uv sync --locked  # Fails if pyproject.toml changed
```

### Issue: Platform mismatch
```dockerfile
# Always exclude .venv from COPY
# It contains platform-specific binaries
```

Add to `.dockerignore`:
```
.venv
```

### Issue: Cache not working
```dockerfile
# Ensure cache mount is correctly specified
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

## UV vs pip: Docker Comparison

### Traditional pip
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### UV (Recommended)
```dockerfile
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

Benefits:
- 10-100x faster dependency resolution
- Deterministic builds via lockfile
- Better caching with bind mounts
- Compiled bytecode option

## FastAPI-Specific Commands

### Development (Hot Reload)
```dockerfile
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
```

### Production
```dockerfile
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Worker count formula: `(2 * CPU_CORES) + 1`
