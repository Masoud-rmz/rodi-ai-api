"""terminal feature --- serve browser-based interactive terminal UI"""

from pathlib import Path


def get_terminal_html() -> str:
    """Load and return the terminal UI HTML from template.html beside this file."""
    template_path = Path(__file__).parent / "template.html"
    return template_path.read_text(encoding="utf-8")
