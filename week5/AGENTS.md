# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Build & Run Commands

All commands must be run from the `week5/` directory. On Windows, use `make` if available or run the underlying commands directly.

- **Run the app**: `PYTHONPATH=. uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000` (or `make run`)
- **Run all tests**: `PYTHONPATH=. pytest -q backend/tests` (or `make test`)
- **Run a single test file**: `PYTHONPATH=. pytest -q backend/tests/test_notes.py`
- **Run a single test**: `PYTHONPATH=. pytest -q backend/tests/test_notes.py::test_create_and_list_notes`
- **Format**: `black . && ruff check . --fix` (or `make format`)
- **Lint**: `ruff check .` (or `make lint`)
- **Seed database**: `PYTHONPATH=. python -c "from backend.app.db import apply_seed_if_needed; apply_seed_if_needed()"`

`PYTHONPATH=.` is required because imports use `backend.app.*` paths from the `week5/` root.

## Dependencies

Managed via Poetry at the repo root (`pyproject.toml`). Install with `pip install -e .[dev]` or `poetry install`. Key dependencies: FastAPI, SQLAlchemy 2.x, Pydantic v2, uvicorn, python-dotenv. Dev: pytest, httpx, black, ruff.

## Code Style

- **black** with line-length 100, targeting Python 3.10–3.12
- **ruff** with line-length 100; enabled rule sets: E, F, I, UP, B; ignored: E501, B008
- Pre-commit hooks enforce black, ruff (`--fix`), trailing-whitespace, and end-of-file-fixer

## Architecture

This is a minimal full-stack app: FastAPI backend + static HTML/JS/CSS frontend, using SQLite via SQLAlchemy.

### Backend (`backend/app/`)

- **`main.py`** — FastAPI app entrypoint. Mounts the static frontend at `/static`, serves `index.html` at `/`, creates DB tables and applies seed on startup, registers routers.
- **`db.py`** — SQLAlchemy engine/session setup. Reads `DATABASE_PATH` from env (default `./data/app.db`). Exposes `get_db()` (FastAPI dependency yielding a session) and `get_session()` (context manager). `apply_seed_if_needed()` runs `data/seed.sql` on first DB creation.
- **`models.py`** — SQLAlchemy ORM models: `Note` (id, title, content) and `ActionItem` (id, description, completed). Both use `declarative_base()`.
- **`schemas.py`** — Pydantic v2 schemas with `from_attributes = True`: `NoteCreate`, `NoteRead`, `ActionItemCreate`, `ActionItemRead`.
- **`routers/`** — One router per resource:
  - `notes.py` — `/notes/` CRUD (list, create, get by id, search by query param `q`)
  - `action_items.py` — `/action-items/` (list, create, complete via `PUT /{id}/complete`)
- **`services/extract.py`** — Utility `extract_action_items(text)` that parses lines ending with `!` or starting with `TODO:`.

### Frontend (`frontend/`)

Plain HTML/JS/CSS served as static files by FastAPI. `app.js` calls the backend API via `fetch()` — no build step or Node toolchain required.

### Tests (`backend/tests/`)

pytest with FastAPI `TestClient`. The `conftest.py` fixture creates a temporary SQLite DB per test (via `tempfile.mkstemp`), overrides `get_db` dependency, and cleans up after. Tests are simple HTTP roundtrip assertions — no mocking.

### Data (`data/`)

- `seed.sql` — DDL + sample rows for notes and action_items, applied automatically on first run
- `app.db` — SQLite database (gitignored in practice; auto-created at startup)

## Configuration

Set `DATABASE_PATH` env var (or use `.env` file in `week5/`) to override the default SQLite path `./data/app.db`.
