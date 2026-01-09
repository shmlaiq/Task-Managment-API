# Conftest Templates

## Basic conftest.py
```python
import pytest

# Shared fixtures available to all tests in directory and subdirectories

@pytest.fixture
def sample_data():
    return {"key": "value", "items": [1, 2, 3]}

@pytest.fixture(autouse=True)
def reset_environment():
    """Runs before every test automatically."""
    yield
    # Cleanup after test
```

## Web Application conftest.py
```python
import pytest
from myapp import create_app, db

@pytest.fixture(scope="session")
def app():
    app = create_app(config="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    client.post("/login", data={"user": "test", "pass": "test"})
    yield client
    client.post("/logout")
```

## FastAPI conftest.py
```python
import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

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
```

## Django conftest.py
```python
import pytest
from django.test import Client
from django.contrib.auth import get_user_model

@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        User = get_user_model()
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return create_user

@pytest.fixture
def authenticated_client(client, user_factory):
    user = user_factory()
    client.force_login(user)
    return client

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
```

## Async conftest.py
```python
import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Override default event loop for session scope."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_db():
    from databases import Database
    db = Database("sqlite:///./test.db")
    await db.connect()
    yield db
    await db.disconnect()
```

## CLI Testing conftest.py
```python
import pytest
from click.testing import CliRunner
from typer.testing import CliRunner as TyperRunner

@pytest.fixture
def cli_runner():
    return CliRunner()

@pytest.fixture
def typer_runner():
    return TyperRunner()

@pytest.fixture
def isolated_cli(cli_runner, tmp_path):
    """CLI runner with isolated filesystem."""
    with cli_runner.isolated_filesystem(temp_dir=tmp_path):
        yield cli_runner
```
