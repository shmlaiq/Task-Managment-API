# CI/CD Integration for Pytest

## Table of Contents
- [GitHub Actions](#github-actions)
- [GitLab CI](#gitlab-ci)
- [Azure DevOps](#azure-devops)
- [CircleCI](#circleci)
- [Jenkins](#jenkins)
- [Pre-commit Hooks](#pre-commit-hooks)

---

## GitHub Actions

### Basic Test Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### Matrix Testing (Multiple Python Versions)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest -v
```

### With Database (PostgreSQL)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
        run: uv run pytest -v
```

### Caching Dependencies

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true  # uv has built-in caching

- name: Install dependencies
  run: uv sync
```

---

## GitLab CI

### Basic Configuration

```yaml
# .gitlab-ci.yml
image: python:3.12

stages:
  - test

variables:
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.uv-cache"

cache:
  paths:
    - .uv-cache/

test:
  stage: test
  before_script:
    - pip install uv
    - uv sync
  script:
    - uv run pytest --cov=src --cov-report=xml --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### Matrix Testing

```yaml
.test-template:
  stage: test
  before_script:
    - pip install uv
    - uv sync
  script:
    - uv run pytest -v

test-py310:
  extends: .test-template
  image: python:3.10

test-py311:
  extends: .test-template
  image: python:3.11

test-py312:
  extends: .test-template
  image: python:3.12
```

### With PostgreSQL

```yaml
test:
  stage: test
  image: python:3.12
  services:
    - postgres:15
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgresql://test:test@postgres:5432/testdb
  before_script:
    - pip install uv
    - uv sync
  script:
    - uv run pytest -v
```

---

## Azure DevOps

### Basic Pipeline

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.12"

  - script: |
      pip install uv
      uv sync
    displayName: "Install dependencies"

  - script: |
      uv run pytest --cov=src --cov-report=xml --junitxml=test-results.xml
    displayName: "Run tests"

  - task: PublishTestResults@2
    inputs:
      testResultsFormat: "JUnit"
      testResultsFiles: "**/test-results.xml"
    condition: always()

  - task: PublishCodeCoverageResults@1
    inputs:
      codeCoverageTool: "Cobertura"
      summaryFileLocation: "**/coverage.xml"
```

---

## CircleCI

### Basic Configuration

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  test:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - restore_cache:
          keys:
            - uv-deps-{{ checksum "pyproject.toml" }}
      - run:
          name: Install uv and dependencies
          command: |
            pip install uv
            uv sync
      - save_cache:
          key: uv-deps-{{ checksum "pyproject.toml" }}
          paths:
            - .venv
      - run:
          name: Run tests
          command: uv run pytest --cov=src --junitxml=test-results/results.xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: test-results

workflows:
  test-workflow:
    jobs:
      - test
```

---

## Jenkins

### Jenkinsfile

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'python:3.12'
        }
    }

    stages {
        stage('Install') {
            steps {
                sh 'pip install uv'
                sh 'uv sync'
            }
        }

        stage('Test') {
            steps {
                sh 'uv run pytest --cov=src --cov-report=xml --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }
    }
}
```

---

## Pre-commit Hooks

### Setup

```bash
uv add pre-commit --dev
```

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        types: [python]
        pass_filenames: false
        always_run: true

      - id: pytest-fast
        name: pytest (fast)
        entry: uv run pytest -x -q --tb=short
        language: system
        types: [python]
        pass_filenames: false

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Install Hooks

```bash
uv run pre-commit install
```

---

## Best Practices

### 1. Separate Unit and Integration Tests

```yaml
# GitHub Actions example
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/unit -v

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests  # Run after unit tests pass
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration -v
```

### 2. Fail Fast in PRs

```yaml
- name: Run tests
  run: pytest -x --tb=short  # Stop on first failure
```

### 3. Parallel Testing in CI

```yaml
- name: Run tests
  run: uv run pytest -n auto  # pytest-xdist should be in dependencies
```

### 4. Required Status Checks

In GitHub:
1. Go to Settings > Branches
2. Add branch protection rule for `main`
3. Enable "Require status checks to pass"
4. Select your test workflow

### 5. Coverage Thresholds

```yaml
- name: Run tests with coverage
  run: uv run pytest --cov=src --cov-fail-under=80
```

---

## Quick Reference

| CI Platform | Config File | Docs |
|-------------|-------------|------|
| GitHub Actions | `.github/workflows/*.yml` | [docs.github.com/actions](https://docs.github.com/actions) |
| GitLab CI | `.gitlab-ci.yml` | [docs.gitlab.com/ee/ci](https://docs.gitlab.com/ee/ci) |
| Azure DevOps | `azure-pipelines.yml` | [docs.microsoft.com/azure/devops](https://docs.microsoft.com/azure/devops) |
| CircleCI | `.circleci/config.yml` | [circleci.com/docs](https://circleci.com/docs) |
| Jenkins | `Jenkinsfile` | [jenkins.io/doc](https://jenkins.io/doc) |
