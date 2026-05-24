## MODIFIED Requirements

### Requirement: Terminal HTML is a separate file loaded by its feature module
The HTML/JS terminal interface SHALL be stored in `rodi_admin/features/terminal/template.html` and loaded at module import time using `Path(__file__).parent / "template.html"`. The Python feature module SHALL export `get_terminal_html() -> str`.

#### Scenario: /terminal returns valid HTML page
- **WHEN** `GET /terminal` is received
- **THEN** response Content-Type is `text/html; charset=utf-8` and body is a complete HTML page with terminal UI

#### Scenario: HTML file is loadable from package
- **WHEN** `rodi_admin.features.terminal` module is imported
- **THEN** `get_terminal_html()` returns a non-empty string without FileNotFoundError

#### Scenario: Terminal UI is functional in browser
- **WHEN** user opens `/terminal` in a browser and starts a session with `bash`
- **THEN** output area receives output and user can type input
