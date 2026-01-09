# Test-Driven Development (TDD) Guide

## Table of Contents
- [TDD Fundamentals](#tdd-fundamentals)
- [Red-Green-Refactor Cycle](#red-green-refactor-cycle)
- [TDD for Functions](#tdd-for-functions)
- [TDD for FastAPI Endpoints](#tdd-for-fastapi-endpoints)
- [TDD for CRUD Operations](#tdd-for-crud-operations)
- [TDD Best Practices](#tdd-best-practices)
- [Common TDD Mistakes](#common-tdd-mistakes)

## TDD Fundamentals

### What is TDD?
Test-Driven Development is a software development approach where you:
1. Write a test BEFORE writing the code
2. Write minimal code to pass the test
3. Refactor while keeping tests green

### The Three Laws of TDD
1. **You may not write production code until you have written a failing unit test**
2. **You may not write more of a unit test than is sufficient to fail**
3. **You may not write more production code than is sufficient to pass the test**

## Red-Green-Refactor Cycle

```
    ┌─────────────────────────────────────────┐
    │                                         │
    ▼                                         │
┌───────┐     ┌───────┐     ┌──────────┐     │
│  RED  │ ──► │ GREEN │ ──► │ REFACTOR │ ────┘
└───────┘     └───────┘     └──────────┘
   │             │              │
   │             │              │
   ▼             ▼              ▼
 Write        Write          Clean up
 failing      minimal        code, keep
 test         code           tests green
```

### Step 1: RED - Write a Failing Test
```python
# tests/test_calculator.py
def test_add_two_numbers():
    # This will FAIL - add() doesn't exist yet
    result = add(2, 3)
    assert result == 5
```

Run the test:
```bash
pytest tests/test_calculator.py -v
# FAILED - NameError: name 'add' is not defined
```

### Step 2: GREEN - Make it Pass (Minimal Code)
```python
# calculator.py
def add(a, b):
    return a + b  # Simplest implementation
```

```python
# tests/test_calculator.py
from calculator import add

def test_add_two_numbers():
    result = add(2, 3)
    assert result == 5
```

Run the test:
```bash
pytest tests/test_calculator.py -v
# PASSED
```

### Step 3: REFACTOR - Improve Code Quality
```python
# calculator.py
def add(a: int | float, b: int | float) -> int | float:
    """Add two numbers and return the result."""
    return a + b
```

Run tests again to ensure they still pass:
```bash
pytest tests/test_calculator.py -v
# PASSED - Refactoring didn't break anything
```

## TDD for Functions

### Example: Building a Password Validator

#### Iteration 1: Minimum Length
```python
# 🔴 RED: Write failing test
def test_password_too_short():
    assert validate_password("abc") == False

def test_password_valid_length():
    assert validate_password("abcdefgh") == True
```

```python
# 🟢 GREEN: Minimal implementation
def validate_password(password: str) -> bool:
    return len(password) >= 8
```

#### Iteration 2: Require Numbers
```python
# 🔴 RED: Add new requirement
def test_password_needs_number():
    assert validate_password("abcdefgh") == False  # No number
    assert validate_password("abcdefg1") == True   # Has number
```

```python
# 🟢 GREEN: Add number check
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True
```

#### Iteration 3: Require Special Character
```python
# 🔴 RED: Add special char requirement
def test_password_needs_special_char():
    assert validate_password("abcdefg1") == False   # No special
    assert validate_password("abcdef1!") == True    # Has special
```

```python
# 🟢 GREEN: Add special char check
import re

def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True
```

```python
# 🔄 REFACTOR: Clean up
import re

def validate_password(password: str) -> bool:
    """Validate password meets security requirements."""
    checks = [
        len(password) >= 8,
        any(c.isdigit() for c in password),
        bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
    ]
    return all(checks)
```

## TDD for FastAPI Endpoints

### Example: Building a Todo API

#### Setup: Test Fixtures
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    from main import app
    with TestClient(app) as c:
        yield c
```

#### Iteration 1: GET /health Endpoint

```python
# 🔴 RED: tests/test_main.py
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

```bash
pytest tests/test_main.py::test_health_check -v
# FAILED - 404 Not Found (endpoint doesn't exist)
```

```python
# 🟢 GREEN: main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

```bash
pytest tests/test_main.py::test_health_check -v
# PASSED
```

#### Iteration 2: GET /todos Endpoint

```python
# 🔴 RED: Test list todos
def test_get_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []
```

```python
# 🟢 GREEN: Minimal implementation
todos = []

@app.get("/todos")
def get_todos():
    return todos
```

#### Iteration 3: POST /todos Endpoint

```python
# 🔴 RED: Test create todo
def test_create_todo(client):
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] == False
    assert "id" in data
```

```python
# 🟢 GREEN: Add create endpoint
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

todos = []
todo_counter = 0

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    global todo_counter
    todo_counter += 1
    new_todo = Todo(id=todo_counter, title=todo.title)
    todos.append(new_todo)
    return new_todo
```

#### Iteration 4: GET /todos/{id} Endpoint

```python
# 🔴 RED: Test get single todo
def test_get_todo_by_id(client):
    # First create a todo
    client.post("/todos", json={"title": "Test"})

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
```

```python
# 🟢 GREEN: Add get by id
from fastapi import HTTPException

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
```

## TDD for CRUD Operations

### Complete CRUD TDD Flow

```python
# tests/test_crud.py
import pytest

class TestUserCRUD:
    """TDD for User CRUD operations."""

    # CREATE
    def test_create_user(self, client):
        response = client.post("/users", json={
            "email": "test@example.com",
            "name": "Test User"
        })
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"

    def test_create_user_duplicate_email(self, client):
        client.post("/users", json={"email": "dup@example.com", "name": "User 1"})
        response = client.post("/users", json={"email": "dup@example.com", "name": "User 2"})
        assert response.status_code == 400

    # READ
    def test_get_user(self, client):
        create_resp = client.post("/users", json={"email": "get@example.com", "name": "Get User"})
        user_id = create_resp.json()["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "get@example.com"

    def test_get_user_not_found(self, client):
        response = client.get("/users/99999")
        assert response.status_code == 404

    def test_list_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    # UPDATE
    def test_update_user(self, client):
        create_resp = client.post("/users", json={"email": "old@example.com", "name": "Old Name"})
        user_id = create_resp.json()["id"]

        response = client.put(f"/users/{user_id}", json={"name": "New Name"})
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    def test_update_user_not_found(self, client):
        response = client.put("/users/99999", json={"name": "Test"})
        assert response.status_code == 404

    # DELETE
    def test_delete_user(self, client):
        create_resp = client.post("/users", json={"email": "del@example.com", "name": "Delete Me"})
        user_id = create_resp.json()["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Verify deleted
        get_resp = client.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

    def test_delete_user_not_found(self, client):
        response = client.delete("/users/99999")
        assert response.status_code == 404
```

## TDD Best Practices

### 1. Test One Thing at a Time
```python
# ✅ Good - Single responsibility
def test_user_email_is_valid():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"

def test_user_email_invalid_raises():
    with pytest.raises(ValueError):
        User(email="invalid")

# ❌ Bad - Testing multiple things
def test_user():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"
    assert user.is_active == True
    assert user.created_at is not None
```

### 2. Use Descriptive Test Names
```python
# ✅ Good
def test_login_fails_with_wrong_password():
    ...

def test_user_cannot_access_admin_routes():
    ...

# ❌ Bad
def test_login():
    ...

def test_auth():
    ...
```

### 3. Arrange-Act-Assert Pattern
```python
def test_add_item_to_cart():
    # Arrange - Setup
    cart = Cart()
    item = Item(name="Widget", price=10.00)

    # Act - Execute
    cart.add(item)

    # Assert - Verify
    assert len(cart.items) == 1
    assert cart.total == 10.00
```

### 4. Keep Tests Independent
```python
# ✅ Good - Each test is independent
@pytest.fixture
def fresh_cart():
    return Cart()

def test_add_single_item(fresh_cart):
    fresh_cart.add(Item("A", 10))
    assert len(fresh_cart.items) == 1

def test_add_multiple_items(fresh_cart):
    fresh_cart.add(Item("A", 10))
    fresh_cart.add(Item("B", 20))
    assert len(fresh_cart.items) == 2
```

### 5. Test Edge Cases
```python
def test_empty_list():
    assert process_items([]) == []

def test_single_item():
    assert process_items([1]) == [1]

def test_negative_numbers():
    assert process_items([-1, -2]) == [-2, -1]

def test_none_input():
    with pytest.raises(TypeError):
        process_items(None)
```

## Common TDD Mistakes

### 1. Writing Too Much Test Code at Once
```python
# ❌ Bad - Too many tests before implementation
def test_user_registration():
    ...
def test_user_login():
    ...
def test_user_logout():
    ...
def test_user_profile():
    ...
# Then trying to implement everything at once

# ✅ Good - One test, one implementation, repeat
def test_user_registration():
    ...
# Implement registration
# Run test, make it pass
# Then move to next test
```

### 2. Testing Implementation Instead of Behavior
```python
# ❌ Bad - Testing how it works internally
def test_uses_dict_for_storage():
    cache = Cache()
    assert isinstance(cache._storage, dict)

# ✅ Good - Testing what it does
def test_cache_stores_and_retrieves_value():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

### 3. Skipping the Refactor Step
```python
# After GREEN phase, always ask:
# - Can this code be cleaner?
# - Are there any duplications?
# - Is the naming clear?
# - Are there any magic numbers/strings?
```

### 4. Not Running Tests After Refactoring
```bash
# ALWAYS run tests after refactoring
pytest -v

# Use watch mode for continuous feedback
pytest-watch
# or
ptw
```

## TDD Workflow Commands

```bash
# Run single test (during RED phase)
uv run pytest tests/test_module.py::test_specific_function -v

# Run all tests (after GREEN/REFACTOR)
uv run pytest -v

# Run with coverage (verify completeness)
uv run pytest --cov=src --cov-report=term-missing

# Watch mode (continuous TDD)
uv add pytest-watch --dev
uv run ptw -- -v

# Run last failed (fix failures quickly)
uv run pytest --lf -v
```
