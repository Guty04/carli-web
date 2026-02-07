# Agent Rules (FastAPI Backend)

## Stack

FastAPI · Python 3.13+ · uv · SQLAlchemy · Pydantic

## Architecture

Layers:
Routes → Services → Repositories → DB

Folders:
configurations, database/models, errors, integrations, repositories,
routes, schemas, services, templates, utils

## Core Principles

- DRY: extract shared logic (services or utils)
- Low coupling: services independent when possible
- High cohesion: one responsibility per service
- Explicit dependencies via injection (no instantiation inside logic)
- No hidden side effects or global state

## Anti-Hallucination

Never invent:

- DB fields
- env vars
- services/repos/utils

When unsure:

- reuse existing patterns
- extend existing modules
- add TODO instead of guessing

## Routes

Must:

- validate with Pydantic schemas
- call ONE service method
- return response schemas
- convert domain errors → HTTPException

Must NOT:

- contain business logic
- access DB
- perform heavy computation

## Services

Must:

- contain business logic only
- orchestrate repos/integrations
- be deterministic & testable

Must NOT:

- use FastAPI objects
- return ORM models

## Repositories

Only:

- DB queries
- persistence
- ORM mapping

Never:

- business logic
- external API calls

## Code Style

- self-documenting names (no generic names)
- functions ≤ ~30 lines
- explicit parameters (no generic dicts)

## Shared Logic

- Pure logic → utils/
- Business rules → services
- No duplication across services

## Logging

Use `logfire` only (already configured).
No standard logging module.

## Testing

Service methods must have:

- unit tests
- failure case
- mocked deps

## Smells to Avoid

- service-to-service chains
- business logic in SQL
- large routes
- deep nesting
- repos returning dicts

## Conventions

Files: snake_case
Classes: PascalCase
Functions: snake_case
Constants: UPPER_SNAKE_CASE

One model/repo per file.

## Commands

Run: `uv run uvicorn src.main:app --reload`
Test: `uv run pytest`
Lint/format: `uv run ruff format . && uv run ruff check . --fix`
Types: `uv run mypy src/`

## Key Files

src/main.py
src/configurations/configuration.py
pyproject.toml

## Golden Rule

Prefer simple, explicit, testable code. Avoid tight coupling and clever abstractions.
