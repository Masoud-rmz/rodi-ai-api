## Context

`api_admin.py` is a working 839-line single-file admin HTTP API for Ubuntu servers. It handles command execution, file reading, interactive PTY sessions, UFW firewall management, and a browser-based terminal UI. The file is used in production in the `rodi` project and is being open-sourced.

Current state problems for open-source release:
- All concerns mixed in one file (not navigable for contributors)
- HTML template embedded as a string literal inside Python source
- Configuration (PORT, MAX_READ_BYTES) as module-level globals
- No community files (LICENSE, CONTRIBUTING, SECURITY)
- No automated CI, no examples for AI agent users

## Goals / Non-Goals

**Goals:**
- Feature-based directory layout: each concern in its own `features/<name>/` folder
- Identical HTTP API surface — no breaking changes for consumers
- Standard GitHub OSS files following the GitHub Standard from `AI learning docs`
- `python3 -m rodi_admin` as the canonical run command
- Centralized config with environment variable overrides
- CI workflow (GitHub Actions) that runs a smoke test

**Non-Goals:**
- Authentication/token system (documented as future work, not implemented here)
- Rate limiting
- Windows/macOS support (UFW is Linux-specific; documented clearly)
- External dependencies — stdlib only

## Decisions

### Decision 1: Feature-based flat modules, not packages

**Choice:** `features/command_execution.py`, `features/file_inspection.py`, etc. (flat modules) rather than `features/command_execution/__init__.py` packages.

**Rationale:** The project is small (each feature is <80 lines). Packages add `__init__.py` boilerplate with no benefit at this scale. Flat modules are easier for first-time contributors to navigate.

**Alternative considered:** Full packages with `__init__.py` per feature — rejected as over-engineering for this size.

### Decision 2: Single `AdminHandler` in `features/http_server.py`

**Choice:** Keep a single `AdminHandler` class that imports from other feature modules and routes to them.

**Rationale:** Splitting routing into per-feature handler classes would require a router abstraction that doesn't exist in `http.server`. The current routing if/elif chain is simple enough to stay in one place, just moved to its own file.

**Alternative considered:** Per-feature mini-handlers composed together — adds complexity without benefit at this scale.

### Decision 3: HTML template as a separate file

**Choice:** `features/terminal/template.html` loaded at import time with `Path(__file__).parent / "template.html"`.

**Rationale:** A 120-line HTML/JS block inside a Python string is hard to edit and can't be linted by HTML tools. Separating it enables syntax highlighting and easier contribution.

### Decision 4: Config via `config.py` with `os.environ` overrides

**Choice:** `config.py` at the root of the package exposes `PORT`, `MAX_READ_BYTES`, `COMMAND_TIMEOUT_SECONDS` as constants, each optionally overridable via environment variables.

**Rationale:** Makes the tool scriptable without code changes. Keeps globals out of feature modules.

## Directory Layout

```
rodi-ai-api/
├── rodi_admin/                   ← installable package
│   ├── __init__.py
│   ├── __main__.py               ← python3 -m rodi_admin entrypoint
│   ├── config.py                 ← PORT, limits, env var overrides
│   ├── features/
│   │   ├── command_execution.py  ← run_command(), /run handler logic
│   │   ├── file_inspection.py    ← safe_read_text_file(), /read /ls /find
│   │   ├── interactive_session.py← InteractiveSession class
│   │   ├── firewall.py           ← open_firewall_port(), cleanup()
│   │   ├── http_server.py        ← AdminHandler, ThreadingHTTPServer
│   │   ├── startup.py            ← banner, port prompts, sudo prompt
│   │   └── terminal/
│   │       ├── __init__.py
│   │       └── template.html
│   └── help_texts.py             ← USER_HELP_TEXT, AI_HELP_TEXT
├── docs/
│   ├── getting-started.md
│   ├── api-reference.md
│   └── architecture.md
├── examples/
│   ├── basic_usage.sh
│   └── ai_agent_usage.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── LICENSE
```

## Risks / Trade-offs

- [Risk] Changing import paths breaks anyone who does `from api_admin import ...` → Mitigation: keep `api_admin.py` as a thin shim that imports from `rodi_admin` for one version, then remove
- [Risk] PTY sessions (`pty.fork`) are Linux-only — breaks on macOS in CI → Mitigation: CI runs on `ubuntu-latest`; document Linux requirement clearly
- [Risk] HTML file not found at runtime if package installed incorrectly → Mitigation: use `importlib.resources` or `Path(__file__).parent` (robust for both direct run and install)

## Migration Plan

1. Create `rodi_admin/` package with all modules
2. Verify `python3 -m rodi_admin` starts and `/help` responds identically
3. Keep old `api_admin.py` in root with a deprecation notice pointing to `rodi_admin`
4. Add all GitHub community files
5. Add CI workflow running smoke test on startup

## Open Questions

- Should `api_admin.py` shim be kept permanently or removed after a transition period? → Keep for v1.0, note removal in v2.0
