def extract_action_items(text: str) -> list[str]:
    """Extract actionable lines from free-form text.

    Args:
        text: Multi-line text containing potential action items.

    Returns:
        A list of lines considered actionable (e.g. TODOs or lines ending with '!').
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    return [line for line in lines if line.endswith("!") or line.lower().startswith("todo:")]
