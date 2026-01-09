# Async SQLModel

## Table of Contents
- [Setup](#setup)
- [Async Engine and Session](#async-engine-and-session)
- [Async CRUD Operations](#async-crud-operations)
- [FastAPI Async Integration](#fastapi-async-integration)
- [Testing Async Code](#testing-async-code)

## Setup

### Installation

```bash
# For SQLite async
uv add sqlmodel aiosqlite

# For PostgreSQL async
uv add sqlmodel asyncpg

# For FastAPI
uv add sqlmodel fastapi "uvicorn[standard]" asyncpg
```

## Async Engine and Session

### Create Async Engine

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# SQLite async
DATABASE_URL = "sqlite+aiosqlite:///database.db"

# PostgreSQL async
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### Create Tables

```python
async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Usage
import asyncio
asyncio.run(create_db_and_tables())
```

### Session Management

```python
from sqlalchemy.ext.asyncio import AsyncSession

# Context manager pattern
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

## Async CRUD Operations

### Models

```python
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
```

### Create

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def create_hero(session: AsyncSession, hero_create: HeroCreate) -> Hero:
    hero = Hero.model_validate(hero_create)
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero
```

### Read

```python
from sqlmodel import select

async def get_hero(session: AsyncSession, hero_id: int) -> Hero | None:
    return await session.get(Hero, hero_id)

async def get_heroes(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> list[Hero]:
    statement = select(Hero).offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

async def get_hero_by_name(session: AsyncSession, name: str) -> Hero | None:
    statement = select(Hero).where(Hero.name == name)
    result = await session.execute(statement)
    return result.scalars().first()
```

### Update

```python
async def update_hero(
    session: AsyncSession,
    hero_id: int,
    hero_update: HeroUpdate
) -> Hero | None:
    hero = await session.get(Hero, hero_id)
    if hero:
        hero_data = hero_update.model_dump(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(hero, key, value)
        session.add(hero)
        await session.commit()
        await session.refresh(hero)
    return hero
```

### Delete

```python
async def delete_hero(session: AsyncSession, hero_id: int) -> bool:
    hero = await session.get(Hero, hero_id)
    if hero:
        await session.delete(hero)
        await session.commit()
        return True
    return False
```

## FastAPI Async Integration

### Database Configuration

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### Main Application

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import heroes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(title="Hero API", lifespan=lifespan)

app.include_router(heroes.router)
```

### Async Router

```python
# app/routers/heroes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Hero, HeroCreate, HeroRead, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.post("/", response_model=HeroRead, status_code=201)
async def create_hero(
    hero: HeroCreate,
    session: AsyncSession = Depends(get_session)
):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero

@router.get("/", response_model=list[HeroRead])
async def read_heroes(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    statement = select(Hero).offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

@router.get("/{hero_id}", response_model=HeroRead)
async def read_hero(
    hero_id: int,
    session: AsyncSession = Depends(get_session)
):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.patch("/{hero_id}", response_model=HeroRead)
async def update_hero(
    hero_id: int,
    hero_update: HeroUpdate,
    session: AsyncSession = Depends(get_session)
):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_update.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)

    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero

@router.delete("/{hero_id}", status_code=204)
async def delete_hero(
    hero_id: int,
    session: AsyncSession = Depends(get_session)
):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    await session.delete(hero)
    await session.commit()
    return None
```

### Async Relationships

```python
from sqlalchemy.orm import selectinload

@router.get("/{hero_id}/with-team", response_model=HeroReadWithTeam)
async def read_hero_with_team(
    hero_id: int,
    session: AsyncSession = Depends(get_session)
):
    statement = (
        select(Hero)
        .options(selectinload(Hero.team))
        .where(Hero.id == hero_id)
    )
    result = await session.execute(statement)
    hero = result.scalars().first()

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

## Testing Async Code

### Test Configuration

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.main import app
from app.database import get_session

# Test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite://"

@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

    await engine.dispose()

@pytest_asyncio.fixture
async def client(async_session: AsyncSession):
    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
```

### Async Test Cases

```python
# tests/test_heroes.py
import pytest

@pytest.mark.asyncio
async def test_create_hero(client):
    response = await client.post("/heroes/", json={
        "name": "Spider-Boy",
        "secret_name": "Pedro Parqueador"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Spider-Boy"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_heroes(client):
    # Create some heroes
    await client.post("/heroes/", json={"name": "Hero1", "secret_name": "S1"})
    await client.post("/heroes/", json={"name": "Hero2", "secret_name": "S2"})

    response = await client.get("/heroes/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_read_hero(client):
    # Create
    create_response = await client.post("/heroes/", json={
        "name": "Spider-Boy",
        "secret_name": "Pedro"
    })
    hero_id = create_response.json()["id"]

    # Read
    response = await client.get(f"/heroes/{hero_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Spider-Boy"

@pytest.mark.asyncio
async def test_read_hero_not_found(client):
    response = await client.get("/heroes/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_hero(client):
    # Create
    create_response = await client.post("/heroes/", json={
        "name": "Old Name",
        "secret_name": "Secret"
    })
    hero_id = create_response.json()["id"]

    # Update
    response = await client.patch(f"/heroes/{hero_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

@pytest.mark.asyncio
async def test_delete_hero(client):
    # Create
    create_response = await client.post("/heroes/", json={
        "name": "To Delete",
        "secret_name": "Secret"
    })
    hero_id = create_response.json()["id"]

    # Delete
    response = await client.delete(f"/heroes/{hero_id}")
    assert response.status_code == 204

    # Verify deleted
    response = await client.get(f"/heroes/{hero_id}")
    assert response.status_code == 404
```

### Run Async Tests

```bash
# Install pytest-asyncio
uv add pytest-asyncio --dev

# Configure in pyproject.toml
# [tool.pytest.ini_options]
# asyncio_mode = "auto"

# Run tests
uv run pytest tests/ -v
```
