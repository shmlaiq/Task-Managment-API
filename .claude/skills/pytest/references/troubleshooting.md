# Pytest Troubleshooting Guide

## Table of Contents
- [Import Errors](#import-errors)
- [Fixture Errors](#fixture-errors)
- [Collection Errors](#collection-errors)
- [Async Test Issues](#async-test-issues)
- [Assertion Errors](#assertion-errors)
- [Performance Issues](#performance-issues)
- [Configuration Issues](#configuration-issues)

---

## Import Errors

### ModuleNotFoundError: No module named 'mypackage'

**Problem:** Python can't find your source code.

**Solutions:**

1. **Add `__init__.py` files:**
```
project/
├── src/
│   ├── __init__.py      # Add this!
│   └── mypackage/
│       ├── __init__.py  # And this!
│       └── module.py
└── tests/
    └── test_module.py
```

2. **Install package in editable mode:**
```bash
pip install -e .
```

3. **Add conftest.py with path fix:**
```python
# tests/conftest.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

4. **Set PYTHONPATH:**
```bash
PYTHONPATH=src pytest
```

5. **Use pyproject.toml:**
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
```

---

### ImportError: cannot import name 'X' from 'module'

**Problem:** Circular imports or wrong import path.

**Solutions:**

1. **Check circular imports:**
```python
# Bad: module_a imports module_b, module_b imports module_a
# Fix: Move shared code to a third module
```

2. **Use relative imports in packages:**
```python
# Inside package, use relative imports
from .utils import helper_function
from ..models import User
```

3. **Import inside function (lazy import):**
```python
def my_function():
    from heavy_module import expensive_class  # Import when needed
    return expensive_class()
```

---

## Fixture Errors

### fixture 'my_fixture' not found

**Problem:** Pytest can't find the fixture.

**Solutions:**

1. **Check conftest.py location:**
```
tests/
├── conftest.py          # Fixtures here are available to all tests below
├── unit/
│   ├── conftest.py      # Fixtures only for unit tests
│   └── test_unit.py
└── integration/
    └── test_integration.py
```

2. **Import fixture from plugin:**
```python
# conftest.py
pytest_plugins = ["mypackage.fixtures"]
```

3. **Check fixture name spelling:**
```python
@pytest.fixture
def database():  # Name must match exactly
    return db

def test_query(database):  # Same name here
    pass
```

---

### ScopeMismatch: fixture scope mismatch

**Problem:** Using a function-scoped fixture in a session-scoped fixture.

**Solution:**
```python
# Wrong: session fixture using function fixture
@pytest.fixture(scope="function")
def db_connection():
    return create_connection()

@pytest.fixture(scope="session")
def app(db_connection):  # Error! scope mismatch
    pass

# Correct: match or use wider scope
@pytest.fixture(scope="session")
def db_connection():
    return create_connection()

@pytest.fixture(scope="session")
def app(db_connection):  # Now works
    pass
```

---

### Fixture teardown not running

**Problem:** Cleanup code after `yield` not executing.

**Solutions:**

1. **Use try/finally:**
```python
@pytest.fixture
def resource():
    r = create_resource()
    try:
        yield r
    finally:
        r.cleanup()  # Always runs
```

2. **Use addfinalizer:**
```python
@pytest.fixture
def resource(request):
    r = create_resource()
    request.addfinalizer(r.cleanup)
    return r
```

---

## Collection Errors

### collected 0 items

**Problem:** No tests found.

**Solutions:**

1. **Check file naming:**
```
# Must start with test_ or end with _test.py
test_module.py  ✓
module_test.py  ✓
tests.py        ✗
my_tests.py     ✗
```

2. **Check function naming:**
```python
def test_something():  ✓
    pass

def check_something():  ✗  # Won't be collected
    pass
```

3. **Check class naming:**
```python
class TestUser:  ✓
    def test_create(self):
        pass

class UserTests:  ✗  # Won't be collected (must start with Test)
    def test_create(self):
        pass
```

4. **Check testpaths configuration:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]  # Make sure this is correct
```

---

### PytestCollectionWarning: cannot collect test class

**Problem:** Test class has `__init__` method.

**Solution:**
```python
# Wrong
class TestUser:
    def __init__(self):  # Remove this!
        self.user = User()

# Correct: use fixtures instead
class TestUser:
    @pytest.fixture
    def user(self):
        return User()

    def test_user(self, user):
        assert user is not None
```

---

## Async Test Issues

### RuntimeWarning: coroutine was never awaited

**Problem:** Async test not properly marked.

**Solution:**
```python
import pytest

# Wrong
async def test_async():  # Missing marker!
    result = await fetch_data()
    assert result

# Correct
@pytest.mark.asyncio
async def test_async():
    result = await fetch_data()
    assert result
```

---

### Event loop is closed

**Problem:** Event loop closed before async operations complete.

**Solution:**
```python
# conftest.py
import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

Or use auto mode:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

### Async fixture not working

**Problem:** Async fixtures need proper setup.

**Solution:**
```python
@pytest.fixture
async def async_client():
    client = await create_async_client()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    result = await async_client.fetch()
    assert result
```

---

## Assertion Errors

### AssertionError with no details

**Problem:** Complex objects don't show diff.

**Solutions:**

1. **Use pytest's assertion introspection:**
```python
# Enable verbose assertions
pytest -vv
```

2. **Add custom repr:**
```python
class User:
    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"
```

3. **Break down complex assertions:**
```python
# Instead of
assert complex_object == expected

# Do this
assert complex_object.field1 == expected.field1
assert complex_object.field2 == expected.field2
```

---

### Floating point comparison fails

**Problem:** `0.1 + 0.2 != 0.3` due to float precision.

**Solution:**
```python
# Wrong
assert 0.1 + 0.2 == 0.3  # Fails!

# Correct
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx(expected, rel=1e-6)
assert result == pytest.approx(expected, abs=0.001)
```

---

## Performance Issues

### Tests are very slow

**Solutions:**

1. **Run in parallel:**
```bash
pip install pytest-xdist
pytest -n auto
```

2. **Use session-scoped fixtures for expensive setup:**
```python
@pytest.fixture(scope="session")
def expensive_resource():
    return create_expensive_thing()  # Created once
```

3. **Skip slow tests in development:**
```python
@pytest.mark.slow
def test_slow_integration():
    pass

# Run without slow tests
pytest -m "not slow"
```

4. **Profile tests:**
```bash
pytest --durations=10  # Show 10 slowest tests
```

---

### Database tests are slow

**Solution:** Use transactions and rollback:
```python
@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()  # Fast cleanup!
    connection.close()
```

---

## Configuration Issues

### pytest.ini vs pyproject.toml vs setup.cfg

**Priority order:**
1. Command line arguments
2. pytest.ini
3. pyproject.toml
4. setup.cfg

**Recommended: pyproject.toml**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
```

---

### Markers not recognized

**Problem:** `PytestUnknownMarkWarning`

**Solution:** Register markers:
```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
    "unit: marks unit tests",
]
```

---

## Quick Debug Commands

```bash
# Verbose output with full tracebacks
pytest -vvv --tb=long

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Show local variables in tracebacks
pytest -l

# Run last failed tests
pytest --lf

# Run failed first, then rest
pytest --ff

# Debug with pdb on failure
pytest --pdb

# Collect tests without running
pytest --collect-only

# Show test durations
pytest --durations=0
```
