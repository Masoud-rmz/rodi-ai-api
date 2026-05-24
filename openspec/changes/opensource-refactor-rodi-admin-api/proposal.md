## Why

`api_admin.py` is a single-file, 839-line admin HTTP API that runs on Ubuntu servers to allow AI agents and operators to remotely execute commands, read files, and manage interactive terminal sessions. The code works but is not structured for maintainability, community contribution, or safe public release. Publishing it as a proper open-source project requires feature-based code separation, standard GitHub community files, and clear security boundaries.

## What Changes

- **BREAKING**: Split monolithic `api_admin.py` into feature-based modules
- Add GitHub community files: `README.md`, `CONTRIBUTING.md`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`
- Add `.github/` directory with issue templates, PR template, and CI workflow
- Add `docs/` with API reference, architecture, and getting-started guides
- Add `examples/` with usage samples for AI agents and operators
- Add `requirements.txt` (stdlib only, no external deps currently)
- Move HTML template out of Python source into `features/terminal/template.html`
- Add `config.py` for centralized configuration (port, limits)
- Add `__main__.py` entrypoint so `python3 -m rodi_admin` works

## Capabilities

### New Capabilities

- `project-structure`: Feature-based directory layout replacing the single-file approach
- `github-community-files`: All standard GitHub OSS files (README, LICENSE, CONTRIBUTING, SECURITY, CHANGELOG, CODE_OF_CONDUCT, issue templates, PR template, CI)
- `api-docs`: Structured documentation in `docs/` covering API reference, architecture, getting-started
- `config-management`: Centralized config module with environment variable support

### Modified Capabilities

- `command-execution`: Move `run_command` + `/run` handler into `features/command_execution/`
- `file-inspection`: Move `safe_read_text_file` + `/read`, `/ls`, `/find` handlers into `features/file_inspection/`
- `interactive-session`: Move `InteractiveSession` + `/session/*` handlers into `features/interactive_session/`
- `terminal-ui`: Move `TERMINAL_HTML` + `/terminal` handler into `features/terminal/`
- `firewall-management`: Move UFW open/close logic into `features/firewall/`
- `http-server`: Move `AdminHandler` + server startup into `features/http_server/`

## Impact

- All code in `api_admin.py` is affected — it is being modularized
- External behavior (HTTP API surface, endpoints, response format) stays identical — no breaking changes for consumers
- Firewall management stays Linux/UFW-specific (documented in README)
- No new external dependencies introduced
