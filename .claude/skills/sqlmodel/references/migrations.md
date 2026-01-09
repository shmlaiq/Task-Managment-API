# Database Migrations with Alembic

## Table of Contents
- [Setup](#setup)
- [Configuration](#configuration)
- [Creating Migrations](#creating-migrations)
- [Running Migrations](#running-migrations)
- [Common Patterns](#common-patterns)
- [CI/CD Integration](#cicd-integration)

## Setup

### Installation

```bash
uv add alembic
```

### Initialize Alembic

```bash
uv run alembic init alembic
```

This creates:
```
alembic/
├── env.py           # Migration environment
├── script.py.mako   # Migration template
├── versions/        # Migration files
alembic.ini          # Configuration
```

## Configuration

### alembic.ini

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .

# Use environment variable for database URL
# sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### alembic/env.py

```python
# alembic/env.py
from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context

# Import all models so they're registered with SQLModel.metadata
from app.models import Hero, Team  # Import all your models here

# this is the Alembic Config object
config = context.config

# Set database URL from environment
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL", "sqlite:///database.db")
)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use SQLModel's metadata for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Creating Migrations

### Autogenerate Migration

```bash
# Create migration from model changes
uv run alembic revision --autogenerate -m "Add hero table"

# With specific message
uv run alembic revision --autogenerate -m "Add age column to hero"
```

### Manual Migration

```bash
# Create empty migration file
uv run alembic revision -m "Add custom indexes"
```

### Example Migration File

```python
# alembic/versions/001_add_hero_table.py
"""Add hero table

Revision ID: abc123
Revises:
Create Date: 2024-01-15 10:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers
revision: str = 'abc123'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'hero',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('secret_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hero_name'), 'hero', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_hero_name'), table_name='hero')
    op.drop_table('hero')
```

## Running Migrations

### Apply Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Apply specific revision
uv run alembic upgrade abc123

# Apply next migration only
uv run alembic upgrade +1
```

### Rollback Migrations

```bash
# Rollback last migration
uv run alembic downgrade -1

# Rollback to specific revision
uv run alembic downgrade abc123

# Rollback all migrations
uv run alembic downgrade base
```

### View Migration Status

```bash
# Show current revision
uv run alembic current

# Show migration history
uv run alembic history

# Show pending migrations
uv run alembic history --indicate-current
```

## Common Patterns

### Add Column

```python
def upgrade() -> None:
    op.add_column('hero', sa.Column('power_level', sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column('hero', 'power_level')
```

### Add Column with Default

```python
def upgrade() -> None:
    op.add_column('hero', sa.Column('is_active', sa.Boolean(), server_default='true'))

def downgrade() -> None:
    op.drop_column('hero', 'is_active')
```

### Rename Column

```python
def upgrade() -> None:
    op.alter_column('hero', 'name', new_column_name='hero_name')

def downgrade() -> None:
    op.alter_column('hero', 'hero_name', new_column_name='name')
```

### Add Index

```python
def upgrade() -> None:
    op.create_index('ix_hero_age', 'hero', ['age'])

def downgrade() -> None:
    op.drop_index('ix_hero_age', table_name='hero')
```

### Add Foreign Key

```python
def upgrade() -> None:
    op.add_column('hero', sa.Column('team_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_hero_team',
        'hero', 'team',
        ['team_id'], ['id']
    )

def downgrade() -> None:
    op.drop_constraint('fk_hero_team', 'hero', type_='foreignkey')
    op.drop_column('hero', 'team_id')
```

### Create Table with Relationships

```python
def upgrade() -> None:
    # Create team table first
    op.create_table(
        'team',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Then create hero with foreign key
    op.create_table(
        'hero',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['team_id'], ['team.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('hero')
    op.drop_table('team')
```

### Data Migration

```python
from sqlalchemy import orm
from app.models import Hero

def upgrade() -> None:
    # Schema change
    op.add_column('hero', sa.Column('full_name', sa.String(), nullable=True))

    # Data migration
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Update existing records
    for hero in session.query(Hero).all():
        hero.full_name = f"{hero.name} ({hero.secret_name})"

    session.commit()

def downgrade() -> None:
    op.drop_column('hero', 'full_name')
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'app/models/**'
      - 'alembic/**'

jobs:
  migrate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync

      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: uv run alembic upgrade head
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

# Run migrations on startup
CMD uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Script for Safe Migrations

```python
# scripts/migrate.py
import sys
from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")

    try:
        # Show current state
        print("Current revision:")
        command.current(alembic_cfg)

        # Show pending migrations
        print("\nPending migrations:")
        command.history(alembic_cfg, indicate_current=True)

        # Apply migrations
        print("\nApplying migrations...")
        command.upgrade(alembic_cfg, "head")

        print("\nMigrations completed successfully!")

    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
```

```bash
uv run python scripts/migrate.py
```

## Best Practices

1. **Always review autogenerated migrations** - They may miss some changes

2. **Test migrations locally first**
   ```bash
   uv run alembic upgrade head
   uv run alembic downgrade -1
   uv run alembic upgrade head
   ```

3. **Use meaningful migration names**
   ```bash
   uv run alembic revision --autogenerate -m "Add email column to user table"
   ```

4. **Keep migrations small** - One logical change per migration

5. **Never edit applied migrations** - Create new ones to fix issues

6. **Backup before production migrations**
   ```bash
   pg_dump -h localhost -U user dbname > backup.sql
   uv run alembic upgrade head
   ```

7. **Use transactions** - Alembic wraps migrations in transactions by default
