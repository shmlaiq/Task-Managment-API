# Pytest Plugins Reference

## Table of Contents
- [pytest-cov (Coverage)](#pytest-cov)
- [pytest-asyncio (Async Testing)](#pytest-asyncio)
- [pytest-mock (Mocking)](#pytest-mock)
- [pytest-xdist (Parallel Testing)](#pytest-xdist)
- [pytest-env (Environment Variables)](#pytest-env)
- [pytest-timeout (Timeouts)](#pytest-timeout)
- [pytest-freezegun (Time Mocking)](#pytest-freezegun)
- [pytest-httpx (HTTP Mocking)](#pytest-httpx)
- [pytest-randomly (Random Order)](#pytest-randomly)

---

## pytest-cov

Code coverage reporting for pytest.

### Installation
```bash
uv add pytest-cov
```

### Usage
```bash
# Basic coverage
pytest --cov=src

# With missing lines report
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html

# Multiple formats
pytest --cov=src --cov-report=term-missing --cov-report=xml --cov-report=html

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

### Configuration (pyproject.toml)
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

---

## pytest-asyncio

Support for async/await test functions.

### Installation
```bash
uv add pytest-asyncio
```

### Usage
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result == expected

@pytest.mark.asyncio
async def test_async_with_fixture(async_client):
    response = await async_client.get("/api/data")
    assert response.status_code == 200
```

### Async Fixtures
```python
@pytest.fixture
async def async_db_session():
    session = await create_async_session()
    yield session
    await session.close()
```

### Configuration (pyproject.toml)
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # No need for @pytest.mark.asyncio
```

---

## pytest-mock

Simplified mocking with the `mocker` fixture.

### Installation
```bash
uv add pytest-mock
```

### Usage
```python
def test_with_mocker(mocker):
    # Patch a function
    mock_api = mocker.patch("module.api_call")
    mock_api.return_value = {"status": "ok"}

    result = my_function()

    assert result["status"] == "ok"
    mock_api.assert_called_once()

def test_spy(mocker):
    # Spy on real function (calls real code but tracks calls)
    spy = mocker.spy(module, "real_function")

    result = module.real_function(42)

    spy.assert_called_once_with(42)

def test_mock_property(mocker):
    # Mock a property
    mocker.patch.object(MyClass, "my_property", new_callable=mocker.PropertyMock, return_value=42)
```

### Async Mocking
```python
@pytest.mark.asyncio
async def test_async_mock(mocker):
    mock_fetch = mocker.patch("module.async_fetch", new_callable=mocker.AsyncMock)
    mock_fetch.return_value = {"data": "test"}

    result = await module.async_fetch()
    assert result["data"] == "test"
```

---

## pytest-xdist

Run tests in parallel across multiple CPUs.

### Installation
```bash
uv add pytest-xdist
```

### Usage
```bash
# Auto-detect CPU count
pytest -n auto

# Specific number of workers
pytest -n 4

# Distribute by file
pytest -n 4 --dist=loadfile

# Distribute by group
pytest -n 4 --dist=loadgroup
```

### Grouping Tests
```python
# Tests with same mark run on same worker
@pytest.mark.xdist_group("database")
def test_db_read():
    pass

@pytest.mark.xdist_group("database")
def test_db_write():
    pass
```

### Configuration
```toml
[tool.pytest.ini_options]
addopts = "-n auto"
```

---

## pytest-env

Set environment variables for tests.

### Installation
```bash
uv add pytest-env
```

### Configuration (pyproject.toml)
```toml
[tool.pytest.ini_options]
env = [
    "DATABASE_URL=sqlite:///test.db",
    "API_KEY=test-key-123",
    "DEBUG=true",
    "D:SECRET_KEY=keep-from-transform",  # D: prefix prevents transformation
]
```

### Usage in Tests
```python
import os

def test_with_env():
    assert os.environ["DATABASE_URL"] == "sqlite:///test.db"
    assert os.environ["API_KEY"] == "test-key-123"
```

---

## pytest-timeout

Set timeouts for tests to prevent hanging.

### Installation
```bash
uv add pytest-timeout
```

### Usage
```bash
# Global timeout (seconds)
pytest --timeout=10

# With method (signal or thread)
pytest --timeout=10 --timeout_method=thread
```

### Per-Test Timeout
```python
@pytest.mark.timeout(5)
def test_slow_operation():
    # Fails if takes more than 5 seconds
    result = slow_function()
    assert result is not None

@pytest.mark.timeout(0)  # Disable timeout
def test_very_slow():
    pass
```

### Configuration
```toml
[tool.pytest.ini_options]
timeout = 10
timeout_method = "thread"
```

---

## pytest-freezegun

Mock datetime for time-dependent tests.

### Installation
```bash
uv add pytest-freezegun
```

### Usage
```python
from datetime import datetime

@pytest.mark.freeze_time("2024-01-15 12:00:00")
def test_frozen_time():
    now = datetime.now()
    assert now.year == 2024
    assert now.month == 1
    assert now.day == 15

def test_with_fixture(freezer):
    freezer.move_to("2024-06-01")
    assert datetime.now().month == 6

    freezer.tick(delta=timedelta(days=1))
    assert datetime.now().day == 2
```

---

## pytest-httpx

Mock HTTP requests for httpx library.

### Installation
```bash
uv add pytest-httpx
```

### Usage
```python
import httpx

@pytest.mark.asyncio
async def test_api_call(httpx_mock):
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"status": "ok"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    assert response.json() == {"status": "ok"}

def test_sync_request(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/submit",
        status_code=201,
        json={"id": 123}
    )

    response = httpx.post("https://api.example.com/submit", json={})
    assert response.status_code == 201
```

---

## pytest-randomly

Randomize test order to catch hidden dependencies.

### Installation
```bash
uv add pytest-randomly
```

### Usage
```bash
# Run with random order
pytest

# Use specific seed (for reproducibility)
pytest -p randomly --randomly-seed=12345

# Disable randomization
pytest -p no:randomly
```

### Configuration
```toml
[tool.pytest.ini_options]
addopts = "--randomly-seed=last"  # Reuse last seed on failure
```

---

## Quick Install All Common Plugins

```bash
uv add pytest-cov pytest-asyncio pytest-mock pytest-xdist pytest-env pytest-timeout
```

## Recommended pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--cov=src",
    "--cov-report=term-missing",
    "-n", "auto",
]
asyncio_mode = "auto"
timeout = 30

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
fail_under = 80
```
