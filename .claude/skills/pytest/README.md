# Pytest Skill

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-8.0+-green.svg)](https://docs.pytest.org/)
[![TDD](https://img.shields.io/badge/TDD-Red--Green--Refactor-red.svg)](#tdd-workflow)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Claude Code skill for Python testing with pytest, emphasizing Test-Driven Development (TDD) practices.

## Features

- **TDD Workflow** - Red-Green-Refactor cycle guidance
- **Test Generation** - Auto-generate test stubs from source code
- **Coverage Analysis** - Check coverage thresholds and identify gaps
- **FastAPI Testing** - Async testing with httpx, dependency overrides
- **Fixture Templates** - Ready-to-use conftest.py templates
- **CI/CD Integration** - GitHub Actions and GitLab CI examples
- **Troubleshooting** - Common errors and solutions

## File Structure

```
pytest/
├── SKILL.md                          # Main skill definition
├── README.md                         # This file
├── scripts/
│   ├── run_tests.py                  # Run pytest with useful defaults
│   ├── generate_tests.py             # Generate test file stubs
│   └── check_coverage.py             # Coverage threshold checker
└── references/
    ├── tdd.md                        # TDD workflow and patterns
    ├── patterns.md                   # Fixtures, mocking, async testing
    ├── conftest_templates.md         # Ready-to-use conftest templates
    ├── fastapi_testing.md            # FastAPI-specific testing
    ├── plugins.md                    # Popular pytest plugins
    ├── troubleshooting.md            # Common errors and fixes
    └── ci_cd.md                      # CI/CD integration examples
```

## Quick Start

### Run Tests

```bash
uv run pytest                      # Run all tests
uv run pytest tests/test_file.py   # Run specific file
uv run pytest -k "test_name"       # Run matching tests
uv run pytest -x                   # Stop on first failure
uv run pytest --lf                 # Run last failed only
```

### Write a Basic Test

```python
def test_addition():
    result = add(2, 3)
    assert result == 5
```

### With Coverage

```bash
uv run pytest --cov=src --cov-report=term-missing
```

## TDD Workflow

This skill emphasizes Test-Driven Development:

```
🔴 RED    → Write a failing test first
🟢 GREEN  → Write minimal code to pass
🔄 REFACTOR → Clean up, keep tests green
```

### Example

```python
# Step 1: 🔴 RED - Write failing test
def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200

# Step 2: 🟢 GREEN - Implement endpoint
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}

# Step 3: 🔄 REFACTOR - Add validation, error handling
```

## Scripts

### run_tests.py

Run pytest with sensible defaults:

```bash
python scripts/run_tests.py                    # All tests
python scripts/run_tests.py tests/test_api.py  # Specific file
python scripts/run_tests.py --cov=src          # With coverage
python scripts/run_tests.py -k "login"         # Pattern match
```

### generate_tests.py

Generate test stubs from source files:

```bash
python scripts/generate_tests.py src/api.py
```

### check_coverage.py

Verify coverage meets thresholds:

```bash
python scripts/check_coverage.py --threshold=80
```

## Popular Plugins

| Plugin | Purpose | Install |
|--------|---------|---------|
| pytest-cov | Code coverage | `uv add pytest-cov` |
| pytest-asyncio | Async test support | `uv add pytest-asyncio` |
| pytest-anyio | Alternative async | `uv add pytest-anyio anyio` |
| pytest-mock | Easier mocking | `uv add pytest-mock` |
| pytest-xdist | Parallel testing | `uv add pytest-xdist` |
| pytest-httpx | Mock httpx requests | `uv add pytest-httpx` |

## Usage Triggers

This skill activates when you:

- Ask to "write tests for this"
- Request "add unit tests"
- Say "test this function"
- Want to "fix the failing test"
- Need to "run pytest"
- Ask to "set up test fixtures"
- Want to "mock this dependency"

## References

| File | Description |
|------|-------------|
| [tdd.md](references/tdd.md) | Complete TDD workflow and patterns |
| [patterns.md](references/patterns.md) | Fixtures, mocking, parametrization |
| [conftest_templates.md](references/conftest_templates.md) | Ready-to-use conftest templates |
| [fastapi_testing.md](references/fastapi_testing.md) | FastAPI async testing, auth, WebSockets |
| [plugins.md](references/plugins.md) | Plugin usage examples |
| [troubleshooting.md](references/troubleshooting.md) | Common errors and solutions |
| [ci_cd.md](references/ci_cd.md) | GitHub Actions, GitLab CI setup |

## Related Skills

- **fastapi** - FastAPI development guide
- **sqlmodel** - Database models with Pydantic + SQLAlchemy

## License

MIT
