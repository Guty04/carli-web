# 🤖 Agent Instructions

This document provides instructions for AI agents working with this codebase.  
The goal is to ensure clean architecture, maintainable code, and zero hallucinated logic.

---

## 📌 Project Overview

- **Type**: FastAPI Backend
- **Language**: Python 3.13+
- **Package Manager**: `uv`

---

## 🏗 Architecture

This project follows a layered architecture:

```e
src/
├── configurations/   # Settings and configuration
├── database/models/  # SQLAlchemy ORM models
├── errors/           # Custom exceptions
├── integrations/     # External services (GitLab, Jira, SonarQube, etc.)
├── repositories/     # Data access layer
├── routes/           # HTTP layer
├── schemas/          # Pydantic validation models
├── services/         # Business logic layer
├── templates/
└── utils/            # Pure helper functions
```

### 🔄 Data Flow

```
Request → Route → Service → Repository → Database
                    ↓
              Response ← Schema validation
```

---

## 🧠 Design Principles

All code generated or modified by an AI agent MUST follow these principles:

### DRY (Don't Repeat Yourself)

- Avoid duplicating logic across services or routes.
- If logic appears more than once, extract it into:
  - a shared service
  - a domain helper
  - or a pure function in `utils/`

### Low Coupling

- Services must NOT directly depend on other services unless necessary.
- No shared mutable state between services.
- Repositories only handle persistence.

### High Cohesion

- Each service should have one responsibility.
- If a service name contains "and", it's likely doing too much.

### Explicit Dependencies

Never instantiate dependencies inside business logic.

❌ Bad:

```python
def create_user():
    repo = UserRepository()
```

✅ Good:

```python
@dataclass
class UserService:
    repo: UserRepository
```

### No Hidden Side Effects

Functions should not:

- Mutate global state
- Modify inputs unexpectedly
- Perform I/O unless it is their explicit responsibility

---

## 🚫 Anti-Hallucination Rules

AI agents must NEVER assume the existence of:

- Database fields not defined in models
- Environment variables not declared in `settings.py`
- Services, repositories, or utilities that do not already exist

### When unsure, the agent MUST:

1. Reuse existing patterns from the codebase
2. Extend an existing service rather than creating a new abstraction
3. Mirror the structure of similar modules

If required information is missing:

- Add a clear `TODO` comment
- Do NOT invent fake fields, APIs, or integrations

---

## 🛣 Routes Layer Rules

Routes are thin controllers.

They MUST:

- Validate input using Pydantic schemas
- Call a single service method
- Return response schemas
- Catch domain exceptions from services and raise `HTTPException` with the appropriate status code

They MUST NOT:

- Contain business logic
- Access the database
- Perform non-trivial calculations
- Let domain exceptions propagate unhandled (no global exception handlers in `main.py`)

---

## 🧠 Services Layer Rules

Services contain business logic only.

They MUST:

- Orchestrate repositories and integrations
- Contain domain-level validations
- Be deterministic and easy to test

They MUST NOT:

- Use FastAPI objects (`Request`, `Response`, `Depends`)
- Return ORM models directly

---

## 🗄 Repository Layer Rules

Repositories are responsible only for:

- Querying the database
- Persisting data
- Mapping ORM models

They MUST NOT:

- Contain business logic
- Call external APIs
- Perform domain validations

---

## ✍️ Self-Documenting Code Rules

Code must be understandable without reading comments.

### Naming

Function names must describe the action:

✅ Good:

- `calculate_pipeline_health_score`
- `get_active_merge_requests`
- `create_project_quality_report`

❌ Avoid:

- `process_data`
- `handle_task`
- `do_action`

### Function Size

- One function = one responsibility
- If longer than ~30 lines → split it

### Parameters

Prefer explicit arguments over generic dicts.

❌ Bad:

```python
def create_user(data: dict):
```

✅ Good:

```python
def create_user(email: str, full_name: str, is_active: bool):
```

---

## 🧩 Shared Logic

If multiple services need the same logic:

- Use `utils/` for pure functions
- Use a domain service for business rules
- NEVER duplicate logic across services

---

## 🧪 Testing Expectations

Every service method should have:

- Unit tests for business rules
- At least one failure scenario
- Mocked repositories or integrations

AI agents should prefer testable code over clever code.

---

## 🚨 Spaghetti Code Smells (AVOID)

- Services calling each other in circular ways
- Business logic inside SQL queries
- Routes longer than 30 lines
- Functions with more than 3 nested blocks
- Repositories returning raw dicts

---

## 📏 Conventions

### Naming

| Element   | Convention         |
| --------- | ------------------ |
| Files     | `snake_case.py`    |
| Classes   | `PascalCase`       |
| Functions | `snake_case`       |
| Constants | `UPPER_SNAKE_CASE` |

### File Organization

- One model/schema/repository per file
- Group related functionality in directories
- Use `__init__.py` to expose public interfaces

---

## ⚙️ Key Commands

```bash
# Run development server
uv run uvicorn src.main:app --reload

# Run tests
uv run pytest

# Format and lint
uv run ruff format . && uv run ruff check . --fix

# Type check
uv run mypy src/
```

---

## 📁 Important Files

- `src/main.py` — Application entry point
- `src/configurations/settings.py` — Environment configuration
- `pyproject.toml` — Dependencies and tool configuration

---

## ✅ Do's and Don'ts

### ✅ Do

- Write tests for new features
- Use type hints everywhere
- Follow existing patterns
- Run pre-commit before committing

### ❌ Don't

- Put business logic in routes
- Skip Pydantic validation
- Commit without tests
- Ignore type errors

---

## 🏆 Golden Rule

If a change makes the system:

- Harder to test
- Harder to understand
- More tightly coupled

It is the wrong design.

Prefer boring, predictable, explicit code over clever solutions.
