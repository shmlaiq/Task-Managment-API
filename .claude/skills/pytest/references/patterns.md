# Pytest Patterns Reference

## Table of Contents
- [Fixture Patterns](#fixture-patterns)
- [Parametrization](#parametrization)
- [Mocking Patterns](#mocking-patterns)
- [Assertion Patterns](#assertion-patterns)
- [Async Testing](#async-testing)
- [Database Testing](#database-testing)

## Fixture Patterns

### Basic Fixtures
```python
import pytest

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}

@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()  # Teardown
```

### Fixture Scopes
```python
@pytest.fixture(scope="function")  # Default: new for each test
@pytest.fixture(scope="class")     # Shared across class
@pytest.fixture(scope="module")    # Shared across module
@pytest.fixture(scope="session")   # Shared across entire session
```

### Fixture Factories
```python
@pytest.fixture
def make_user():
    def _make_user(name="default", role="user"):
        return User(name=name, role=role)
    return _make_user

def test_admin(make_user):
    admin = make_user(name="admin", role="admin")
    assert admin.role == "admin"
```

### Fixture with Parameters
```python
@pytest.fixture(params=["mysql", "postgres", "sqlite"])
def database(request):
    db = connect_to(request.param)
    yield db
    db.disconnect()
```

## Parametrization

### Basic Parametrize
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

### Multiple Parameters
```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    # Runs 4 times: (1,10), (1,20), (2,10), (2,20)
    assert multiply(x, y) == x * y
```

### Parametrize with IDs
```python
@pytest.mark.parametrize("input,expected", [
    pytest.param("hello", 5, id="simple"),
    pytest.param("", 0, id="empty"),
    pytest.param("  ", 2, id="whitespace"),
])
def test_length(input, expected):
    assert len(input) == expected
```

## Mocking Patterns

### Basic Mock
```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_service = Mock()
    mock_service.get_data.return_value = {"key": "value"}

    result = process(mock_service)
    mock_service.get_data.assert_called_once()
```

### Patch Decorator
```python
@patch("module.external_api")
def test_api_call(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = my_function()
    assert result["status"] == "ok"
```

### Patch Context Manager
```python
def test_with_context():
    with patch("module.get_time") as mock_time:
        mock_time.return_value = 12345
        assert get_timestamp() == 12345
```

### pytest-mock (mocker fixture)
```python
def test_with_mocker(mocker):
    mock_fn = mocker.patch("module.expensive_call")
    mock_fn.return_value = "cached"
    assert fetch_data() == "cached"
```

### Mock Async Functions
```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_mock():
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {"data": "test"}
    result = await mock_client.fetch()
    assert result["data"] == "test"
```

## Assertion Patterns

### Exception Testing
```python
def test_raises():
    with pytest.raises(ValueError):
        raise_value_error()

def test_raises_with_match():
    with pytest.raises(ValueError, match=r"invalid.*input"):
        validate("")

def test_raises_capture():
    with pytest.raises(CustomError) as exc_info:
        risky_operation()
    assert exc_info.value.code == 500
```

### Approximate Comparisons
```python
def test_float():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert result == pytest.approx(expected, rel=1e-3)
    assert result == pytest.approx(expected, abs=0.01)
```

### Collection Assertions
```python
def test_collections():
    assert set(result) == {1, 2, 3}
    assert sorted(items) == [1, 2, 3]
    assert "key" in result_dict
    assert len(items) == 5
```

## Async Testing

### pytest-asyncio
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch()
    assert result == expected

@pytest.fixture
async def async_client():
    client = await create_client()
    yield client
    await client.close()
```

### Async Fixtures
```python
@pytest.fixture
async def db_session():
    session = await create_async_session()
    yield session
    await session.rollback()
    await session.close()
```

## Database Testing

### Transactional Tests
```python
@pytest.fixture
def db_session(db_connection):
    transaction = db_connection.begin()
    yield db_connection
    transaction.rollback()  # Auto-cleanup
```

### SQLAlchemy Pattern
```python
@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### Factory Boy Integration
```python
import factory
from factory.alchemy import SQLAlchemyModelFactory

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = Session

    name = factory.Faker("name")
    email = factory.Faker("email")

def test_user_creation(db_session):
    user = UserFactory()
    assert user.id is not None
```
