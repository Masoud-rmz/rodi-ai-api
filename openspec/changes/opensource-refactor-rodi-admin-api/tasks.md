## 1. Package scaffold

- [ ] 1.1 Create `rodi_admin/` directory with `__init__.py` (version string)
- [ ] 1.2 Create `rodi_admin/__main__.py` as the entrypoint (`python3 -m rodi_admin`)
- [ ] 1.3 Create `rodi_admin/config.py` with PORT, MAX_READ_BYTES, COMMAND_TIMEOUT_SECONDS and env var overrides
- [ ] 1.4 Create `rodi_admin/help_texts.py` with USER_HELP_TEXT and AI_HELP_TEXT constants
- [ ] 1.5 Create `rodi_admin/features/` directory structure with empty `__init__.py` files

## 2. Feature modules — extract from api_admin.py

- [ ] 2.1 Create `rodi_admin/features/command_execution.py` — move `run_command()` and GET/POST `/run` handler logic
- [ ] 2.2 Create `rodi_admin/features/file_inspection.py` — move `safe_read_text_file()` and `/read`, `/ls`, `/find` handler logic
- [ ] 2.3 Create `rodi_admin/features/interactive_session.py` — move `InteractiveSession` class and `SESSIONS` registry
- [ ] 2.4 Create `rodi_admin/features/firewall.py` — move UFW functions (`open_firewall_port`, `cleanup`, `verify_firewall_port_open`, `verify_sudo_password`, `prompt_required_sudo_password`)
- [ ] 2.5 Create `rodi_admin/features/startup.py` — move `prompt_available_port`, `prompt_port_number`, `is_port_in_use`, `get_listening_service_on_port`, `print_startup_banner`, `get_local_ips`

## 3. Terminal UI feature

- [ ] 3.1 Create `rodi_admin/features/terminal/` directory with `__init__.py`
- [ ] 3.2 Move `TERMINAL_HTML` string content to `rodi_admin/features/terminal/template.html`
- [ ] 3.3 Add `get_terminal_html() -> str` function in `rodi_admin/features/terminal/__init__.py` that reads `template.html` via `Path(__file__).parent`

## 4. HTTP server feature

- [ ] 4.1 Create `rodi_admin/features/http_server.py` with `AdminHandler` class
- [ ] 4.2 Wire `do_GET` to delegate to feature handler functions from step 2 and 3
- [ ] 4.3 Wire `do_POST` to delegate to feature handler functions from step 2
- [ ] 4.4 Wire `do_OPTIONS` for CORS preflight
- [ ] 4.5 Add `start_server(port: int, sudo_pass: str) -> None` function

## 5. Backward-compatible shim

- [ ] 5.1 Update root `api_admin.py` to print deprecation notice then call `rodi_admin.__main__.main()`
- [ ] 5.2 Verify `python3 api_admin.py` still starts the server correctly

## 6. Smoke test

- [ ] 6.1 Create `tests/test_smoke.py` — import all feature modules and verify no ImportError
- [ ] 6.2 Add test: start server on random port, call `/help`, assert `status: running` in response, stop server

## 7. GitHub community files

- [ ] 7.1 Create `LICENSE` (MIT, 2024, project author)
- [ ] 7.2 Create `README.md` following GitHub Standard with badges, features, requirements, install, usage, API table, license
- [ ] 7.3 Create `CONTRIBUTING.md` with setup steps, code style, PR process
- [ ] 7.4 Create `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
- [ ] 7.5 Create `SECURITY.md` with vulnerability reporting contact and LAN-only scope warning
- [ ] 7.6 Create `CHANGELOG.md` with initial v1.0.0 entry (Keep a Changelog format)

## 8. GitHub automation

- [ ] 8.1 Create `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] 8.2 Create `.github/ISSUE_TEMPLATE/feature_request.md`
- [ ] 8.3 Create `.github/PULL_REQUEST_TEMPLATE.md` with checklist
- [ ] 8.4 Create `.github/workflows/ci.yml` — runs on ubuntu-latest, imports package, runs smoke test

## 9. Documentation

- [ ] 9.1 Create `docs/getting-started.md` — prerequisites, install, start, verify
- [ ] 9.2 Create `docs/api-reference.md` — all 10 endpoints with method, params, example request/response
- [ ] 9.3 Create `docs/architecture.md` — directory tree with one-line description per module
- [ ] 9.4 Create `examples/basic_usage.sh` — curl examples for common operations
- [ ] 9.5 Create `examples/ai_agent_usage.md` — usage guide for AI coding agents

## 10. Final validation

- [ ] 10.1 Run `python3 -m rodi_admin --help` and verify output matches original
- [ ] 10.2 Run smoke test suite and confirm all pass
- [ ] 10.3 Verify directory tree matches `docs/architecture.md`
- [ ] 10.4 Update `openspec/specs/` root-level specs if any are created during implementation
