# modules/parser.py
def parse_criteria(criteria_str: str):
    """Split a semicolon‑separated criteria string → list of clean, lower‑case rules."""
    return [c.strip().lower() for c in criteria_str.split(';') if c.strip()]
