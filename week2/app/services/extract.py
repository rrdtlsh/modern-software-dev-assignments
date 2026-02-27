from __future__ import annotations

import os
import re
from typing import List

from dotenv import load_dotenv
from ollama import chat
from pydantic import BaseModel, ValidationError

load_dotenv()

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# Model used for LLM-based extraction. Override via OLLAMA_EXTRACT_MODEL env.
OLLAMA_EXTRACT_MODEL = os.getenv("OLLAMA_EXTRACT_MODEL", "llama3.1:8b")

# -----------------------------------------------------------------------------
# LLM Response Schemas (API contracts for structured output)
# -----------------------------------------------------------------------------


class ActionItemsOutput(BaseModel):
    """
    Schema for LLM action-item extraction response.
    Ollama returns JSON matching this structure when using format=model_json_schema().
    """

    items: list[str]


# -----------------------------------------------------------------------------
# Heuristic Extraction Patterns
# -----------------------------------------------------------------------------

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    """True if the line looks like an action item (bullet, keyword prefix, or checkbox)."""
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    """
    Extract action items using heuristics (bullets, keywords, imperative sentences).
    No LLM required.
    """
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from text using an LLM via Ollama.
    Uses structured output (ActionItemsOutput schema). Falls back to heuristic
    extraction on LLM/network errors or malformed JSON.
    """
    if not text or not text.strip():
        return []

    try:
        response = chat(
            model=OLLAMA_EXTRACT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": _build_extraction_prompt(text),
                }
            ],
            format=ActionItemsOutput.model_json_schema(),
            options={"temperature": 0},
        )
        content = response.message.content
        if not content:
            return extract_action_items(text)
        parsed = ActionItemsOutput.model_validate_json(content)
        return list(parsed.items) if parsed.items else []
    except ValidationError:
        # Malformed or schema-mismatched JSON from LLM
        return extract_action_items(text)
    except OSError:
        # Ollama unavailable, connection refused, socket errors
        return extract_action_items(text)
    except Exception:
        # Catch-all for other failures (e.g. httpx.ConnectError, timeouts)
        return extract_action_items(text)


def _build_extraction_prompt(text: str) -> str:
    """Build the LLM prompt for action-item extraction."""
    return f"""Extract all action items, tasks, or to-dos from the following text.
Return them as a JSON object with a single key "items" containing an array of strings.
Each string should be one action item, trimmed and concise. Return an empty array if none found.

Text:
{text}"""


def _looks_imperative(sentence: str) -> bool:
    """True if the sentence starts with an imperative verb (e.g. add, fix, update)."""
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
