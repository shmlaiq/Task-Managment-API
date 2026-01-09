# FastAPI + SQLModel Integration

## Table of Contents
- [Project Setup](#project-setup)
- [TDD Workflow](#tdd-workflow)
- [Complete CRUD API](#complete-crud-api)
- [Dependency Injection](#dependency-injection)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Project Setup

### Installation

```bash
uv init my-api && cd my-api
uv add sqlmodel fastapi "uvicorn[standard]"
uv add pytest httpx --dev
```

### Minimal Example

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Model
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

# Database
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

# App
app = FastAPI(title="Hero API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes/", response_model=list[Hero])
def read_heroes(session: Session = Depends(get_session)):
    return session.exec(select(Hero)).all()
```

```bash
uv run fastapi dev main.py
```

## TDD Workflow

### Step 1: Write Test First (RED)

```python
# tests/test_heroes.py
def test_create_hero(client):
    response = client.post("/heroes/", json={
        "name": "Spider-Boy",
        "secret_name": "Pedro Parqueador",
        "age": 16
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Spider-Boy"
    assert "id" in data
```

```bash
uv run pytest tests/test_heroes.py::test_create_hero -v
# FAILED - endpoint doesn't exist yet
```

### Step 2: Implement (GREEN)

```python
# app/models.py
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id: int

# app/routers/heroes.py
@router.post("/", response_model=HeroRead, status_code=201)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

```bash
uv run pytest tests/test_heroes.py::test_create_hero -v
# PASSED
```

### Step 3: Refactor

Add validation, indexes, better error handling while keeping tests green.

## Complete CRUD API

### Models

```python
# app/models/hero.py
from sqlmodel import Field, SQLModel

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
```

### Router

```python
# app/routers/heroes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models.hero import Hero, HeroCreate, HeroRead, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])

# CREATE
@router.post("/", response_model=HeroRead, status_code=201)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# READ (list with pagination)
@router.get("/", response_model=list[HeroRead])
def read_heroes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    statement = select(Hero).offset(skip).limit(limit)
    return session.exec(statement).all()

# READ (single)
@router.get("/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# UPDATE (partial)
@router.patch("/{hero_id}", response_model=HeroRead)
def update_hero(
    hero_id: int,
    hero_update: HeroUpdate,
    session: Session = Depends(get_session)
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_update.model_dump(exclude_unset=True)
    hero.sqlmodel_update(hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# DELETE
@router.delete("/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return None
```

### Main App

```python
# app/main.py
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routers import heroes

app = FastAPI(title="Hero API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(heroes.router)

@app.get("/health")
def health():
    return {"status": "healthy"}
```

### Database Module

```python
# app/database.py
from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

## Dependency Injection

### Session Dependency

```python
from fastapi import Depends
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/heroes/")
def read_heroes(session: Session = Depends(get_session)):
    return session.exec(select(Hero)).all()
```

### Repository Pattern

```python
# app/repositories/hero.py
from sqlmodel import Session, select
from app.models.hero import Hero, HeroCreate, HeroUpdate

class HeroRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, hero_create: HeroCreate) -> Hero:
        hero = Hero.model_validate(hero_create)
        self.session.add(hero)
        self.session.commit()
        self.session.refresh(hero)
        return hero

    def get(self, hero_id: int) -> Hero | None:
        return self.session.get(Hero, hero_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Hero]:
        statement = select(Hero).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, hero_id: int, hero_update: HeroUpdate) -> Hero | None:
        hero = self.get(hero_id)
        if hero:
            hero_data = hero_update.model_dump(exclude_unset=True)
            hero.sqlmodel_update(hero_data)
            self.session.add(hero)
            self.session.commit()
            self.session.refresh(hero)
        return hero

    def delete(self, hero_id: int) -> bool:
        hero = self.get(hero_id)
        if hero:
            self.session.delete(hero)
            self.session.commit()
            return True
        return False

# Dependency
def get_hero_repo(session: Session = Depends(get_session)) -> HeroRepository:
    return HeroRepository(session)

# Usage in router
@router.get("/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, repo: HeroRepository = Depends(get_hero_repo)):
    hero = repo.get(hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

## Error Handling

```python
# app/exceptions.py
from fastapi import HTTPException

class HeroNotFound(HTTPException):
    def __init__(self, hero_id: int):
        super().__init__(
            status_code=404,
            detail=f"Hero with id {hero_id} not found"
        )

class HeroAlreadyExists(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=400,
            detail=f"Hero with name '{name}' already exists"
        )

# Usage
@router.get("/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HeroNotFound(hero_id)
    return hero
```

## Testing

### Test Configuration

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### Test Cases

```python
# tests/test_heroes.py
class TestCreateHero:
    def test_create_hero_success(self, client):
        response = client.post("/heroes/", json={
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Spider-Boy"
        assert "id" in data

    def test_create_hero_with_age(self, client):
        response = client.post("/heroes/", json={
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": 30
        })
        assert response.status_code == 201
        assert response.json()["age"] == 30

    def test_create_hero_missing_name(self, client):
        response = client.post("/heroes/", json={
            "secret_name": "Unknown"
        })
        assert response.status_code == 422


class TestReadHeroes:
    def test_read_heroes_empty(self, client):
        response = client.get("/heroes/")
        assert response.status_code == 200
        assert response.json() == []

    def test_read_heroes_with_data(self, client):
        # Create heroes first
        client.post("/heroes/", json={"name": "Hero1", "secret_name": "S1"})
        client.post("/heroes/", json={"name": "Hero2", "secret_name": "S2"})

        response = client.get("/heroes/")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestReadHero:
    def test_read_hero_success(self, client):
        # Create
        create_response = client.post("/heroes/", json={
            "name": "Spider-Boy",
            "secret_name": "Pedro"
        })
        hero_id = create_response.json()["id"]

        # Read
        response = client.get(f"/heroes/{hero_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Spider-Boy"

    def test_read_hero_not_found(self, client):
        response = client.get("/heroes/999")
        assert response.status_code == 404


class TestUpdateHero:
    def test_update_hero_success(self, client):
        # Create
        create_response = client.post("/heroes/", json={
            "name": "Old Name",
            "secret_name": "Secret"
        })
        hero_id = create_response.json()["id"]

        # Update
        response = client.patch(f"/heroes/{hero_id}", json={"name": "New Name"})
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    def test_update_hero_not_found(self, client):
        response = client.patch("/heroes/999", json={"name": "Test"})
        assert response.status_code == 404


class TestDeleteHero:
    def test_delete_hero_success(self, client):
        # Create
        create_response = client.post("/heroes/", json={
            "name": "To Delete",
            "secret_name": "Secret"
        })
        hero_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/heroes/{hero_id}")
        assert response.status_code == 204

        # Verify deleted
        response = client.get(f"/heroes/{hero_id}")
        assert response.status_code == 404

    def test_delete_hero_not_found(self, client):
        response = client.delete("/heroes/999")
        assert response.status_code == 404
```

### Run Tests

```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=app --cov-report=term-missing
```

## Project Structure

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── database.py          # Engine and session
│   ├── models/
│   │   ├── __init__.py
│   │   └── hero.py          # SQLModel models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── heroes.py        # API endpoints
│   └── repositories/        # Optional: data layer
│       ├── __init__.py
│       └── hero.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   └── test_heroes.py       # Test cases
├── pyproject.toml
└── .env
```
