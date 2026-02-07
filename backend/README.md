# Carli Backend

## Description

Add your project description here.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- [pre-commit](https://pre-commit.com/)
- [GGA](https://github.com/Gentleman-Programming/gentleman-guardian-angel) (Gentleman Guardian Angel)

## Installation

### uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### pre-commit

```bash
uv tool install pre-commit
```

### GGA

```bash
git clone https://github.com/Gentleman-Programming/gentleman-guardian-angel.git
cd gga
./install.sh
```

## Quick Start

```bash
# Clone the repository
git clone https://{{ github_url  }}/{{ project_name }}.git
cd {{ project_name }}

# Create virtual environment and install dependencies
uv sync

# Run the application
fastapi run dev
```

## Development

### Setup

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test types
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m e2e
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check . --fix

# Type checking
uv run mypy src/
```

## Project Structure

```
backend/
├── src/
│   ├── main.py              # Application entry point
│   ├── configurations/      # Config and settings
│   ├── database/            # Database models and connections
│   ├── enums/               # Enumerations
│   ├── errors/              # Custom exceptions
│   ├── repositories/        # Data access layer
│   ├── routes/              # API endpoints
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/
│   ├── e2e/                 # End-to-end tests
│   ├── integration/         # Integration tests
│   └── unit/                # Unit tests
├── Dockerfile
├── pyproject.toml
└── README.md
```
