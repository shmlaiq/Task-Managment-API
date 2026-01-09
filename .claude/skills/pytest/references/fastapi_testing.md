# FastAPI Testing Reference

## Table of Contents
- [Quick Start](#quick-start)
- [TestClient vs AsyncClient](#testclient-vs-asyncclient)
- [Dependency Overrides](#dependency-overrides)
- [Database Testing](#database-testing)
- [Authentication Testing](#authentication-testing)
- [WebSocket Testing](#websocket-testing)
- [Background Tasks Testing](#background-tasks-testing)
- [File Upload Testing](#file-upload-testing)

---

## Quick Start

### Sync Testing with TestClient
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

### Async Testing with httpx (Recommended)
```python
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

---

## TestClient vs AsyncClient

| Feature | TestClient | AsyncClient |
|---------|------------|-------------|
| Sync tests | Yes | No |
| Async tests | No | Yes |
| Lifespan events | Yes | Yes (with ASGITransport) |
| WebSocket | Yes | No |
| Import | `fastapi.testclient` | `httpx` |

### When to Use Each

**TestClient:**
- Simple sync endpoints
- WebSocket testing
- Quick prototyping

**AsyncClient:**
- Async endpoints
- Testing with async database sessions
- Better for async-heavy applications

---

## Dependency Overrides

### Basic Override Pattern
```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

def get_db():
    return RealDatabase()

@app.get("/items")
def read_items(db = Depends(get_db)):
    return db.get_items()

# In tests
def get_test_db():
    return MockDatabase()

def test_read_items():
    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    response = client.get("/items")
    assert response.status_code == 200
    app.dependency_overrides.clear()
```

### Fixture-Based Override
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_db

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

### Override Settings
```python
from functools import lru_cache
from app.config import Settings, get_settings

def get_settings_override():
    return Settings(
        database_url="sqlite:///./test.db",
        debug=True,
        secret_key="test-secret"
    )

@pytest.fixture(autouse=True)
def override_settings():
    app.dependency_overrides[get_settings] = get_settings_override
    yield
    app.dependency_overrides.clear()
```

---

## Database Testing

### SQLAlchemy with Test Database
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

### Async SQLAlchemy
```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture
async def async_db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        yield session

    await engine.dispose()
```

---

## Authentication Testing

### JWT Token Testing
```python
import pytest
from app.auth import create_access_token

@pytest.fixture
def auth_headers():
    token = create_access_token(data={"sub": "testuser"})
    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint(client, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200

def test_unauthorized(client):
    response = client.get("/protected")
    assert response.status_code == 401
```

### Override Current User
```python
from app.deps import get_current_user

@pytest.fixture
def authenticated_client(db_session):
    test_user = User(id=1, username="testuser")

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
```

### OAuth2 Testing
```python
@pytest.fixture
def oauth_client(client):
    # Login and get token
    response = client.post(
        "/token",
        data={"username": "test", "password": "test"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
```

---

## WebSocket Testing

### Basic WebSocket Test
```python
from fastapi.testclient import TestClient

def test_websocket():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("hello")
            data = websocket.receive_text()
            assert data == "Message: hello"
```

### WebSocket with Authentication
```python
def test_websocket_auth(auth_token):
    with TestClient(app) as client:
        with client.websocket_connect(
            f"/ws?token={auth_token}"
        ) as websocket:
            data = websocket.receive_json()
            assert data["type"] == "connected"
```

### WebSocket JSON Messages
```python
def test_websocket_json():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json({"action": "subscribe", "channel": "updates"})
            response = websocket.receive_json()
            assert response["status"] == "subscribed"
```

---

## Background Tasks Testing

### Mock Background Tasks
```python
from unittest.mock import patch, MagicMock
from fastapi import BackgroundTasks

def test_endpoint_with_background_task(client):
    with patch("app.tasks.send_email") as mock_send:
        response = client.post(
            "/users",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 201
        mock_send.assert_called_once_with("test@example.com")
```

### Override BackgroundTasks
```python
@pytest.fixture
def mock_background_tasks():
    tasks = []

    class MockBackgroundTasks:
        def add_task(self, func, *args, **kwargs):
            tasks.append((func, args, kwargs))

    return MockBackgroundTasks(), tasks

def test_background_task_added(client, mock_background_tasks):
    mock_bg, tasks = mock_background_tasks
    # Override in your endpoint or test setup
    response = client.post("/action")
    assert len(tasks) == 1
```

---

## File Upload Testing

### Single File Upload
```python
def test_upload_file(client):
    files = {"file": ("test.txt", b"file content", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
```

### Multiple Files
```python
def test_upload_multiple(client):
    files = [
        ("files", ("file1.txt", b"content1", "text/plain")),
        ("files", ("file2.txt", b"content2", "text/plain")),
    ]
    response = client.post("/upload-multiple", files=files)
    assert response.status_code == 200
    assert len(response.json()["filenames"]) == 2
```

### File with Form Data
```python
def test_upload_with_form(client):
    files = {"file": ("test.pdf", b"pdf content", "application/pdf")}
    data = {"description": "Test document"}
    response = client.post("/upload", files=files, data=data)
    assert response.status_code == 200
```

---

## Complete conftest.py for FastAPI

```python
import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.deps import get_current_user
from app.auth import create_access_token

# Database fixtures
@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

# Client fixtures
@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
async def async_client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()

# Auth fixtures
@pytest.fixture
def test_user(db_session):
    from app.models import User
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_token(test_user):
    return create_access_token(data={"sub": test_user.username})

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def authenticated_client(client, test_user):
    def override_get_current_user():
        return test_user
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)
```

---

## Required Dependencies

```bash
pip install pytest pytest-asyncio httpx pytest-cov
```

### pytest.ini / pyproject.toml
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```
