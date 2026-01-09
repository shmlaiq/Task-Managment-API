# Testing FastAPI Applications

## Table of Contents
- [TDD Approach](#tdd-approach)
- [Setup](#setup)
- [Basic Testing](#basic-testing)
- [Async Testing](#async-testing)
- [Database Testing](#database-testing)
- [Authentication Testing](#authentication-testing)
- [Mocking](#mocking)
- [Test Organization](#test-organization)

## TDD Approach

**Always follow Test-Driven Development when building FastAPI endpoints:**

### Red-Green-Refactor Cycle
```
🔴 RED    → Write a failing test for the endpoint
🟢 GREEN  → Create minimal endpoint to pass the test
🔄 REFACTOR → Improve code quality, keep tests green
```

### TDD Workflow for FastAPI

#### Step 1: Write Test First (RED)
```python
# tests/test_items.py
def test_create_item(client):
    response = client.post("/items/", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
```

```bash
uv run pytest tests/test_items.py::test_create_item -v
# FAILED - 404 Not Found (endpoint doesn't exist yet)
```

#### Step 2: Implement Endpoint (GREEN)
```python
# app/routers/items.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    price: float

class Item(BaseModel):
    id: int
    name: str
    price: float

@router.post("/items/", status_code=201, response_model=Item)
def create_item(item: ItemCreate):
    return Item(id=1, **item.model_dump())
```

```bash
uv run pytest tests/test_items.py::test_create_item -v
# PASSED
```

#### Step 3: Refactor (Keep Tests Green)
```python
# Add database storage, validation, error handling
# Run tests after each change to ensure they still pass
```

### TDD for Complete CRUD

```python
# Write tests in this order, implementing each before moving to next:

# 1. CREATE
def test_create_item(client):
    response = client.post("/items/", json={"name": "Test", "price": 10.0})
    assert response.status_code == 201

# 2. READ (single)
def test_get_item(client):
    # First create, then get
    create_resp = client.post("/items/", json={"name": "Test", "price": 10.0})
    item_id = create_resp.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

# 3. READ (list)
def test_list_items(client):
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 4. UPDATE
def test_update_item(client):
    create_resp = client.post("/items/", json={"name": "Old", "price": 10.0})
    item_id = create_resp.json()["id"]
    response = client.put(f"/items/{item_id}", json={"name": "New", "price": 20.0})
    assert response.status_code == 200
    assert response.json()["name"] == "New"

# 5. DELETE
def test_delete_item(client):
    create_resp = client.post("/items/", json={"name": "Delete Me", "price": 10.0})
    item_id = create_resp.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

# 6. Error cases
def test_get_item_not_found(client):
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_create_item_invalid_data(client):
    response = client.post("/items/", json={"name": ""})  # Missing price
    assert response.status_code == 422
```

### TDD Best Practices for FastAPI

1. **Test endpoints, not internal functions** - Focus on API behavior
2. **Use fixtures for test client** - Keep tests clean and consistent
3. **Test error cases** - 404, 422, 401, 403 responses
4. **Test edge cases** - Empty lists, null values, boundaries
5. **Run tests after every change** - Catch regressions immediately

## Setup

### Installation
```bash
uv add pytest pytest-asyncio httpx --dev
```

### Configuration

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

```python
# pyproject.toml alternative
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Basic Testing

```python
# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Widget", "price": 9.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget"
    assert data["price"] == 9.99
    assert "id" in data

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_validation_error():
    response = client.post(
        "/items/",
        json={"name": "Widget"}  # Missing required 'price'
    )
    assert response.status_code == 422
```

## Async Testing

```python
# tests/test_async.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_read_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_create_and_get_item(async_client: AsyncClient):
    # Create
    response = await async_client.post(
        "/items/",
        json={"name": "Test Item", "price": 19.99}
    )
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Get
    response = await async_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
```

## Database Testing

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(test_engine):
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def async_client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()

# tests/test_users.py
@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data  # Password should not be returned

@pytest.mark.asyncio
async def test_create_duplicate_user(async_client: AsyncClient):
    # Create first user
    await async_client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123"
        }
    )

    # Try to create duplicate
    response = await async_client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
```

## Authentication Testing

```python
# tests/conftest.py
from app.core.security import create_access_token

@pytest.fixture
def auth_headers():
    """Generate auth headers for a test user."""
    token = create_access_token({"sub": "1", "username": "testuser"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def authenticated_user(db_session, async_client):
    """Create a user and return auth headers."""
    # Create user in DB
    from app.crud import user as user_crud
    from app.schemas import UserCreate

    user_data = UserCreate(
        email="auth@example.com",
        username="authuser",
        password="password123"
    )
    user = await user_crud.create(db_session, user_data)
    await db_session.commit()

    # Generate token
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}

# tests/test_protected.py
@pytest.mark.asyncio
async def test_protected_route_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_route_authorized(async_client: AsyncClient, authenticated_user):
    response = await async_client.get(
        "/users/me",
        headers=authenticated_user
    )
    assert response.status_code == 200
    assert response.json()["email"] == "auth@example.com"

@pytest.mark.asyncio
async def test_login(async_client: AsyncClient, db_session):
    # Create user first
    from app.crud import user as user_crud
    from app.schemas import UserCreate

    await user_crud.create(
        db_session,
        UserCreate(email="login@example.com", username="loginuser", password="password123")
    )
    await db_session.commit()

    # Test login
    response = await async_client.post(
        "/auth/token",
        data={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient):
    response = await async_client.post(
        "/auth/token",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
```

## Mocking

```python
# tests/test_mocking.py
from unittest.mock import patch, AsyncMock
import pytest

# Mock external service
@pytest.mark.asyncio
async def test_external_api_call(async_client: AsyncClient):
    mock_response = {"weather": "sunny", "temp": 72}

    with patch("app.services.weather.fetch_weather", new_callable=AsyncMock) as mock:
        mock.return_value = mock_response

        response = await async_client.get("/weather/NYC")
        assert response.status_code == 200
        assert response.json()["weather"] == "sunny"
        mock.assert_called_once_with("NYC")

# Mock dependency
@pytest.mark.asyncio
async def test_with_mocked_dependency(async_client: AsyncClient):
    async def mock_get_current_user():
        return {"id": 1, "username": "mockuser", "role": "admin"}

    from app.core.auth import get_current_user
    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = await async_client.get("/admin/dashboard")
    assert response.status_code == 200

    app.dependency_overrides.clear()

# Mock with pytest-mock
@pytest.mark.asyncio
async def test_send_email(async_client: AsyncClient, mocker):
    mock_send = mocker.patch("app.services.email.send_email", new_callable=AsyncMock)

    response = await async_client.post(
        "/users/",
        json={"email": "new@example.com", "username": "newuser", "password": "pass123"}
    )

    assert response.status_code == 201
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert call_args[0][0] == "new@example.com"  # First positional arg
```

## Test Organization

```
tests/
├── conftest.py           # Shared fixtures
├── test_main.py          # Root endpoint tests
├── routers/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_items.py
│   └── test_auth.py
├── services/
│   ├── __init__.py
│   └── test_email.py
└── utils/
    ├── __init__.py
    └── test_helpers.py
```

### Fixtures by Scope

```python
# tests/conftest.py
import pytest

# Session-scoped: created once for all tests
@pytest.fixture(scope="session")
async def test_engine():
    # Database engine setup
    ...

# Function-scoped (default): created for each test
@pytest.fixture
async def db_session(test_engine):
    # Fresh session for each test
    ...

# Module-scoped: created once per test file
@pytest.fixture(scope="module")
async def sample_data(test_engine):
    # Seed data for a group of tests
    ...
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("email,expected_status", [
    ("valid@example.com", 201),
    ("invalid-email", 422),
    ("", 422),
    ("a@b.c", 201),
])
@pytest.mark.asyncio
async def test_create_user_email_validation(async_client, email, expected_status):
    response = await async_client.post(
        "/users/",
        json={"email": email, "username": "test", "password": "password123"}
    )
    assert response.status_code == expected_status

@pytest.mark.parametrize("method,path,status", [
    ("GET", "/", 200),
    ("GET", "/health", 200),
    ("GET", "/nonexistent", 404),
    ("POST", "/items/", 422),  # Missing body
])
def test_routes(client, method, path, status):
    response = getattr(client, method.lower())(path)
    assert response.status_code == status
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific file
uv run pytest tests/test_users.py

# Run specific test
uv run pytest tests/test_users.py::test_create_user

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run only marked tests
uv run pytest -m "slow"  # Requires @pytest.mark.slow decorator

# Run in parallel (requires pytest-xdist)
uv run pytest -n auto
```
