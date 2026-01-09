# SQLModel Basics

## Table of Contents
- [Installation](#installation)
- [Creating Models](#creating-models)
- [Database Connection](#database-connection)
- [CRUD Operations](#crud-operations)
- [Field Types and Validation](#field-types-and-validation)
- [Queries](#queries)

## Installation

```bash
# Initialize new project
uv init my-project && cd my-project

# Install SQLModel
uv add sqlmodel

# With database drivers
uv add sqlmodel aiosqlite      # SQLite async
uv add sqlmodel asyncpg        # PostgreSQL async
uv add sqlmodel psycopg2-binary  # PostgreSQL sync
```

## Creating Models

### Basic Model

```python
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
```

### Model Inheritance Pattern

```python
from sqlmodel import Field, SQLModel

# Base with shared fields (NOT a table)
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

# Database table
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# Request body schema
class HeroCreate(HeroBase):
    pass

# Response schema
class HeroRead(HeroBase):
    id: int

# Update schema (all optional)
class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
```

### Why This Pattern?

| Model | Purpose | `table=True` |
|-------|---------|--------------|
| `HeroBase` | Shared fields | No |
| `Hero` | Database table | Yes |
| `HeroCreate` | Request validation | No |
| `HeroRead` | Response model | No |
| `HeroUpdate` | Partial updates | No |

## Database Connection

### SQLite

```python
from sqlmodel import create_engine, SQLModel, Session

# File-based
DATABASE_URL = "sqlite:///database.db"

# In-memory (for testing)
DATABASE_URL = "sqlite://"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL logging

# Create all tables
SQLModel.metadata.create_all(engine)
```

### PostgreSQL

```python
# Sync
DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"

# Async
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

engine = create_engine(DATABASE_URL)
```

### Session Management

```python
from sqlmodel import Session

# Context manager (recommended)
with Session(engine) as session:
    hero = Hero(name="Spider-Boy", secret_name="Pedro")
    session.add(hero)
    session.commit()

# Manual management
session = Session(engine)
try:
    hero = Hero(name="Spider-Boy", secret_name="Pedro")
    session.add(hero)
    session.commit()
finally:
    session.close()
```

## CRUD Operations

### Create

```python
def create_hero(session: Session, name: str, secret_name: str, age: int | None = None) -> Hero:
    hero = Hero(name=name, secret_name=secret_name, age=age)
    session.add(hero)
    session.commit()
    session.refresh(hero)  # Get auto-generated ID
    return hero

# From Pydantic model
def create_hero_from_schema(session: Session, hero_create: HeroCreate) -> Hero:
    hero = Hero.model_validate(hero_create)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Bulk create
def create_heroes(session: Session, heroes: list[HeroCreate]) -> list[Hero]:
    db_heroes = [Hero.model_validate(h) for h in heroes]
    session.add_all(db_heroes)
    session.commit()
    for hero in db_heroes:
        session.refresh(hero)
    return db_heroes
```

### Read

```python
from sqlmodel import select

# Get by ID
def get_hero(session: Session, hero_id: int) -> Hero | None:
    return session.get(Hero, hero_id)

# Get all
def get_heroes(session: Session) -> list[Hero]:
    statement = select(Hero)
    return session.exec(statement).all()

# Get with pagination
def get_heroes_paginated(session: Session, skip: int = 0, limit: int = 10) -> list[Hero]:
    statement = select(Hero).offset(skip).limit(limit)
    return session.exec(statement).all()

# Get first match
def get_hero_by_name(session: Session, name: str) -> Hero | None:
    statement = select(Hero).where(Hero.name == name)
    return session.exec(statement).first()

# Get one (raises if not found or multiple)
def get_hero_by_name_strict(session: Session, name: str) -> Hero:
    statement = select(Hero).where(Hero.name == name)
    return session.exec(statement).one()
```

### Update

```python
# Direct update
def update_hero(session: Session, hero_id: int, name: str) -> Hero | None:
    hero = session.get(Hero, hero_id)
    if hero:
        hero.name = name
        session.add(hero)
        session.commit()
        session.refresh(hero)
    return hero

# Update from schema (partial)
def update_hero_partial(session: Session, hero_id: int, hero_update: HeroUpdate) -> Hero | None:
    hero = session.get(Hero, hero_id)
    if hero:
        hero_data = hero_update.model_dump(exclude_unset=True)
        hero.sqlmodel_update(hero_data)
        session.add(hero)
        session.commit()
        session.refresh(hero)
    return hero
```

### Delete

```python
def delete_hero(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if hero:
        session.delete(hero)
        session.commit()
        return True
    return False

# Bulk delete
def delete_heroes_by_age(session: Session, min_age: int) -> int:
    statement = select(Hero).where(Hero.age >= min_age)
    heroes = session.exec(statement).all()
    count = len(heroes)
    for hero in heroes:
        session.delete(hero)
    session.commit()
    return count
```

## Field Types and Validation

### Common Field Options

```python
from sqlmodel import Field
from datetime import datetime
from enum import Enum

class HeroStatus(str, Enum):
    active = "active"
    retired = "retired"
    deceased = "deceased"

class Hero(SQLModel, table=True):
    # Primary key (auto-increment)
    id: int | None = Field(default=None, primary_key=True)

    # Required string with index
    name: str = Field(index=True)

    # Required unique string
    email: str = Field(unique=True)

    # Optional with default
    age: int | None = Field(default=None)

    # With validation
    power_level: int = Field(ge=0, le=100, default=50)

    # String with max length
    bio: str | None = Field(default=None, max_length=500)

    # Enum field
    status: HeroStatus = Field(default=HeroStatus.active)

    # Timestamp with default
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key
    team_id: int | None = Field(default=None, foreign_key="team.id")
```

### Field Validation Options

| Option | Description | Example |
|--------|-------------|---------|
| `default` | Default value | `Field(default=0)` |
| `default_factory` | Callable for default | `Field(default_factory=datetime.utcnow)` |
| `primary_key` | Primary key | `Field(primary_key=True)` |
| `foreign_key` | Foreign key reference | `Field(foreign_key="table.column")` |
| `unique` | Unique constraint | `Field(unique=True)` |
| `index` | Create index | `Field(index=True)` |
| `nullable` | Allow NULL | `Field(nullable=True)` |
| `max_length` | String max length | `Field(max_length=100)` |
| `ge` | Greater or equal | `Field(ge=0)` |
| `le` | Less or equal | `Field(le=100)` |
| `gt` | Greater than | `Field(gt=0)` |
| `lt` | Less than | `Field(lt=100)` |
| `regex` | Pattern match | `Field(regex=r"^[a-z]+$")` |

## Queries

### Basic Queries

```python
from sqlmodel import select, col

# Select all
statement = select(Hero)
heroes = session.exec(statement).all()

# Select specific columns
statement = select(Hero.name, Hero.age)
results = session.exec(statement).all()  # Returns tuples

# Where clause
statement = select(Hero).where(Hero.name == "Spider-Boy")
hero = session.exec(statement).first()

# Multiple conditions (AND)
statement = select(Hero).where(Hero.age >= 18).where(Hero.age <= 65)
# or
statement = select(Hero).where(Hero.age >= 18, Hero.age <= 65)
```

### Advanced Queries

```python
from sqlmodel import or_, and_, col, func

# OR conditions
statement = select(Hero).where(
    or_(Hero.name == "Spider-Boy", Hero.name == "Deadpond")
)

# AND with OR
statement = select(Hero).where(
    and_(
        Hero.age >= 18,
        or_(Hero.status == "active", Hero.status == "training")
    )
)

# LIKE / ILIKE
statement = select(Hero).where(col(Hero.name).contains("Spider"))
statement = select(Hero).where(col(Hero.name).startswith("Spider"))
statement = select(Hero).where(col(Hero.name).endswith("Boy"))

# IN
statement = select(Hero).where(col(Hero.name).in_(["Spider-Boy", "Deadpond"]))

# IS NULL / IS NOT NULL
statement = select(Hero).where(Hero.age == None)
statement = select(Hero).where(Hero.age != None)

# Order by
statement = select(Hero).order_by(Hero.name)
statement = select(Hero).order_by(col(Hero.age).desc())

# Limit and offset
statement = select(Hero).offset(10).limit(5)

# Count
statement = select(func.count()).select_from(Hero)
count = session.exec(statement).one()

# Aggregations
statement = select(func.avg(Hero.age)).select_from(Hero)
avg_age = session.exec(statement).one()

# Group by
statement = select(Hero.team_id, func.count(Hero.id)).group_by(Hero.team_id)
results = session.exec(statement).all()
```

### Query Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `.all()` | Get all results | `list[Model]` |
| `.first()` | Get first or None | `Model | None` |
| `.one()` | Get exactly one (raises if 0 or >1) | `Model` |
| `.one_or_none()` | Get one or None (raises if >1) | `Model | None` |
