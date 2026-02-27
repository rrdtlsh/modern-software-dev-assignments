The README must include:
- Project overview
- Tech stack
- Setup and run instructions
- API endpoints and their functionality
- Frontend usage
- Instructions for running tests (if available)

Assume this is a FastAPI backend with a minimal HTML frontend.

# Action Item Extractor

A FastAPI web application that converts free-form notes into actionable checklist items. Supports both heuristic-based extraction and LLM-powered extraction via Ollama.

## Project Overview

The Action Item Extractor lets users paste notes (meeting minutes, to-do lists, etc.) and automatically extract structured action items. Extracted items can be saved to a SQLite database, marked as done, and associated with notes. The app offers two extraction modes:

- **Heuristic extraction** — Rule-based parsing of bullets, keywords (`todo:`, `action:`, `next:`), checkboxes (`[ ]`), and imperative sentences.
- **LLM extraction** — Uses a local LLM (Ollama) for semantic understanding. Falls back to heuristics if the LLM is unavailable or returns invalid output.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Database | SQLite |
| LLM | Ollama (local models) |
| Frontend | Minimal HTML, CSS, vanilla JavaScript |
| Python | 3.10+ |
| Dependencies | Pydantic, python-dotenv, ollama |

## Setup and Run

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) (or follow the root repo setup)
- [Ollama](https://ollama.com/) (optional, for LLM extraction)

### Install Dependencies

From the **project root** (not `week2/`):

```bash
poetry install --no-interaction
```

### Run the Server

```bash
poetry run uvicorn week2.app.main:app --reload
```

Then open http://127.0.0.1:8000/ in your browser.

### Optional: Ollama for LLM Extraction

To use "Extract with LLM", install and run Ollama, then pull a model:

```bash
ollama pull llama3.2:3b
```

Override the model via the `OLLAMA_EXTRACT_MODEL` environment variable (default: `llama3.2:3b`).

## API Endpoints

### Action Items (`/action-items`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/action-items/extract` | Extract action items using heuristics. Body: `{"text": "...", "save_note": bool}`. Returns `{"note_id": int|null, "items": [{"id": int, "text": str}]}`. |
| POST | `/action-items/extract-llm` | Extract action items using the LLM. Same request/response as `/extract`. Falls back to heuristics on LLM failure. |
| GET | `/action-items` | List all action items. Query: `note_id` (optional) to filter by note. |
| POST | `/action-items/{id}/done` | Mark an action item done/undone. Body: `{"done": bool}`. |

### Notes (`/notes`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | List all notes (id, content, created_at). |
| GET | `/notes/{note_id}` | Get a single note by ID. Returns 404 if not found. |
| POST | `/notes` | Create a note. Body: `{"content": "..."}`. |

### Other

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the frontend HTML. |

## Frontend Usage

The minimal HTML frontend at `week2/frontend/index.html` provides:

1. **Notes textarea** — Paste or type notes.
2. **Save as note** — Checkbox to persist the raw text as a note when extracting.
3. **Extract** — Uses heuristic extraction. Results appear as checkboxes; toggle them to mark items done.
4. **Extract with LLM** — Uses the LLM for extraction. Same UI as Extract. Requires Ollama if you want the LLM path; otherwise falls back to heuristics.
5. **List All Notes** — Fetches and displays all saved notes below the main form.

Static assets (HTML, CSS, JS) are served from `/static` and the root path serves the main page.

## Running Tests

From the **project root**:

```bash
poetry run pytest week2/tests/ -v
```

Tests live in `week2/tests/test_extract.py` and cover:

- Heuristic extraction (bullets, checkboxes, numbered lists)
- LLM extraction success (mocked)
- LLM extraction with empty input
- LLM extraction fallback on malformed JSON

Ollama is mocked in tests, so no running LLM is required.
