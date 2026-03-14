BULLET_PREFIXES = ("- ", "* ", "• ", "-", "*", "•")


def _remove_bullet(line: str) -> str:
    cleaned = line.strip()
    for prefix in BULLET_PREFIXES:
        if cleaned.startswith(prefix):
            return cleaned[len(prefix) :].strip()
    return cleaned


def extract_action_items(text: str) -> list[str]:
    results: list[str] = []
    for line in text.splitlines():
        cleaned = _remove_bullet(line.strip())
        if not cleaned:
            continue
        normalized = cleaned.lower()
        if normalized.startswith("todo:") or normalized.startswith("action:"):
            results.append(cleaned)
        elif cleaned.endswith("!"):
            results.append(cleaned)
    return results


