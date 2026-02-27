import pytest
from unittest.mock import patch, MagicMock

from ..app.services.extract import extract_action_items, extract_action_items_llm


# --- Tests for extract_action_items (heuristic) ---


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# --- Tests for extract_action_items_llm ---


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_success(mock_chat):
    """Successful extraction when LLM returns valid JSON."""
    mock_response = MagicMock()
    mock_response.message.content = '{"items": ["Fix bug", "Add tests", "Update docs"]}'
    mock_chat.return_value = mock_response

    result = extract_action_items_llm("Meeting notes: Fix bug. Add tests. Update docs.")

    assert result == ["Fix bug", "Add tests", "Update docs"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_empty_input(mock_chat):
    """Empty input returns empty list without calling LLM."""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    mock_chat.assert_not_called()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_malformed_json_fallback(mock_chat):
    """Invalid or malformed JSON falls back to heuristic extraction."""
    mock_response = MagicMock()
    mock_response.message.content = "not valid json"
    mock_chat.return_value = mock_response

    text = "- [ ] Set up database\n* implement API"
    result = extract_action_items_llm(text)

    # Fallback to heuristic extraction should find bullet items
    assert "Set up database" in result
    assert "implement API" in result
