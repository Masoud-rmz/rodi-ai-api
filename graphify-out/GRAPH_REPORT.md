# Graph Report - rodi-ai-api  (2026-08-21)

## Corpus Check
- 43 files · ~14,379 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 370 nodes · 440 edges · 31 communities (29 shown, 2 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `81df4da2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AdminHandler
- __main__.py
- http_server.py
- .do_POST
- API Reference
- GitHub Repository Setup Checklist
- RODI AI Server Agent
- test_smoke.py
- design.md
- ADDED Requirements
- tasks.md
- ADDED Requirements
- Getting Started
- Requirement: File inspection is an isolated feature module
- Requirement: InteractiveSession class is an isolated feature module
- Requirement: Feature-based package layout
- AI Agent Usage Guide
- bug_report.md
- proposal.md
- Requirement: Command execution is an isolated feature module
- ADDED Requirements
- Requirement: Firewall management is an isolated feature module
- Requirement: HTTP server and routing are in an isolated feature module
- Contributor Covenant Code of Conduct
- Requirement: Terminal HTML is a separate file loaded by its feature module
- feature_request.md
- PULL_REQUEST_TEMPLATE.md
- basic_usage.sh
- __init__.py

## God Nodes (most connected - your core abstractions)
1. `AdminHandler` - 22 edges
2. `RODI AI Server Agent` - 13 edges
3. `API Reference` - 12 edges
4. `create_admin_server()` - 11 edges
5. `RodiAdminThreadingServer` - 10 edges
6. `main()` - 9 edges
7. `run_command()` - 9 edges
8. `InteractiveSession` - 8 edges
9. `get_local_ips()` - 7 edges
10. `prompt_available_port()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `test_run_command_echo()` --calls--> `run_command()`  [EXTRACTED]
  tests/test_smoke.py → rodi_admin/features/command_execution.py
- `TestAdminHandlerClientTimeout` --uses--> `RodiAdminThreadingServer`  [INFERRED]
  tests/test_http_server.py → rodi_admin/features/http_server.py
- `TestAdminServerFactory` --uses--> `RodiAdminThreadingServer`  [INFERRED]
  tests/test_http_server.py → rodi_admin/features/http_server.py
- `TestClientReadTimeoutIntegration` --uses--> `RodiAdminThreadingServer`  [INFERRED]
  tests/test_http_server.py → rodi_admin/features/http_server.py
- `TestHelpEndpointTimeouts` --uses--> `RodiAdminThreadingServer`  [INFERRED]
  tests/test_http_server.py → rodi_admin/features/http_server.py

## Import Cycles
- None detected.

## Communities (31 total, 2 thin omitted)

### Community 0 - "AdminHandler"
Cohesion: 0.07
Nodes (30): AdminHandler, _client_read_timeout_payload(), create_admin_server(), HTTP request handler — routes all endpoints to feature modules., Write JSON response before the HTTP request line has been parsed., Skip access log when the request line was never parsed., Return 408 when stdlib request read times out (Python 3.13+)., Apply client read timeout so idle connections cannot block a worker thread. (+22 more)

### Community 1 - "__main__.py"
Cohesion: 0.08
Nodes (36): cleanup_firewall_port(), open_firewall_port(), prompt_required_sudo_password(), firewall --- UFW port management for startup and graceful shutdown, Remove the UFW rule for the given port.  Called via atexit.      Args:, Prompt the user until a valid non-empty sudo password is provided.      Return, Check whether UFW reports the given TCP port as allowed.      Args:         p, Open a TCP port in UFW; exit if the rule cannot be confirmed.      Args: (+28 more)

### Community 2 - "http_server.py"
Cohesion: 0.12
Nodes (23): config --- centralized configuration with environment variable overrides, Read an integer from environment; fall back to default on invalid value., _read_int_env(), handle_run_get(), handle_run_post(), command_execution --- run shell commands and handle /run endpoint, Handle GET /run?cmd=... request.      Args:         params: Parsed query stri, Handle POST /run with JSON body {"cmd": "..."}.      Args:         body: Pars (+15 more)

### Community 3 - ".do_POST"
Cohesion: 0.09
Nodes (19): Serialise data as JSON and write the HTTP response.          Args:, Read and parse the JSON request body.          Returns:             Tuple of, Route all POST requests to the appropriate feature handler., handle_session_output_get(), handle_session_send_post(), handle_session_start_post(), handle_session_stop_post(), InteractiveSession (+11 more)

### Community 4 - "API Reference"
Cohesion: 0.08
Nodes (22): Code style, Contributing to rodi_admin, Feature requests, Pull request process, Questions?, Running tests, Setup, API Reference (+14 more)

### Community 5 - "GitHub Repository Setup Checklist"
Cohesion: 0.09
Nodes (19): [1.0.0] - 2026-05-24, Added, Changed, Changelog, Deprecated, Planned, [Unreleased], About (repository homepage) (+11 more)

### Community 6 - "RODI AI Server Agent"
Cohesion: 0.13
Nodes (15): API Reference, Architecture, CLI options, Contributing, Environment variables, Features, Installation, License (+7 more)

### Community 7 - "test_smoke.py"
Cohesion: 0.15
Nodes (12): get_terminal_html(), terminal feature --- serve browser-based interactive terminal UI, Load and return the terminal UI HTML from template.html beside this file., test_smoke --- import and basic HTTP smoke tests for rodi_admin.  Tests are di, All feature modules must be importable without raising ImportError., Start server on a random port, call /help, assert status == 'running'., run_command('echo hello') must return success=True and stdout containing 'hello', get_terminal_html() must return a non-empty string. (+4 more)

### Community 8 - "design.md"
Cohesion: 0.17
Nodes (11): Context, Decision 1: Feature-based flat modules, not packages, Decision 2: Single `AdminHandler` in `features/http_server.py`, Decision 3: HTML template as a separate file, Decision 4: Config via `config.py` with `os.environ` overrides, Decisions, Directory Layout, Goals / Non-Goals (+3 more)

### Community 9 - "ADDED Requirements"
Cohesion: 0.18
Nodes (10): ADDED Requirements, Requirement: CI workflow runs on push, Requirement: GitHub issue and PR templates, Requirement: Standard GitHub OSS files present, Scenario: Bug report template has required fields, Scenario: CI passes on clean code, Scenario: LICENSE file exists with MIT license, Scenario: PR template has checklist (+2 more)

### Community 10 - "tasks.md"
Cohesion: 0.18
Nodes (10): 10. Final validation, 1. Package scaffold, 2. Feature modules — extract from api_admin.py, 3. Terminal UI feature, 4. HTTP server feature, 5. Backward-compatible shim, 6. Smoke test, 7. GitHub community files (+2 more)

### Community 11 - "ADDED Requirements"
Cohesion: 0.20
Nodes (9): ADDED Requirements, Requirement: AI agent usage example, Requirement: API reference document, Requirement: Architecture document, Requirement: Getting started guide, Scenario: AI agent can use examples without modification, Scenario: Architecture doc matches actual code, Scenario: Every endpoint is documented (+1 more)

### Community 12 - "Getting Started"
Cohesion: 0.25
Nodes (7): Configuration via environment variables, Getting Started, Install, Prerequisites, Start the server, Stop the server, Verify it works

### Community 13 - "Requirement: File inspection is an isolated feature module"
Cohesion: 0.25
Nodes (7): MODIFIED Requirements, Requirement: File inspection is an isolated feature module, Scenario: /find searches by name pattern, Scenario: /ls lists directory contents, Scenario: /read on missing file returns 404, Scenario: /read returns file content, Scenario: /read truncates large files

### Community 14 - "Requirement: InteractiveSession class is an isolated feature module"
Cohesion: 0.25
Nodes (7): MODIFIED Requirements, Requirement: InteractiveSession class is an isolated feature module, Scenario: Input can be sent to running session, Scenario: Output of unknown session_id returns 404, Scenario: Session output is pollable, Scenario: Session starts and returns session_id, Scenario: Session stop cleans up from registry

### Community 15 - "Requirement: Feature-based package layout"
Cohesion: 0.25
Nodes (7): ADDED Requirements, Requirement: Backward-compatible shim, Requirement: Feature-based package layout, Scenario: Each feature is an independent module, Scenario: HTML template is a separate file, Scenario: Old invocation still works, Scenario: Package is runnable as a module

### Community 16 - "AI Agent Usage Guide"
Cohesion: 0.29
Nodes (6): AI Agent Usage Guide, Interactive Sessions, Quick Start, Reading Files, Running Commands, Tips for AI Agents

### Community 17 - "bug_report.md"
Cohesion: 0.29
Nodes (6): Actual Behavior, Additional Context, Bug Description, Environment, Expected Behavior, Steps to Reproduce

### Community 18 - "proposal.md"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 19 - "Requirement: Command execution is an isolated feature module"
Cohesion: 0.29
Nodes (6): MODIFIED Requirements, Requirement: Command execution is an isolated feature module, Scenario: Command timeout returns error response, Scenario: GET /run?cmd= executes command and returns stdout, Scenario: Missing cmd parameter returns 400, Scenario: POST /run with JSON body executes command

### Community 20 - "ADDED Requirements"
Cohesion: 0.29
Nodes (6): ADDED Requirements, Requirement: Centralized config module, Requirement: Environment variable overrides, Scenario: Default config works without environment variables, Scenario: Invalid env var value falls back to default, Scenario: Port overridden via environment variable

### Community 21 - "Requirement: Firewall management is an isolated feature module"
Cohesion: 0.29
Nodes (6): MODIFIED Requirements, Requirement: Firewall management is an isolated feature module, Scenario: Port is closed in UFW on exit, Scenario: Port is opened in UFW on startup, Scenario: UFW rule not confirmed causes exit, Scenario: Wrong sudo password prompts again

### Community 22 - "Requirement: HTTP server and routing are in an isolated feature module"
Cohesion: 0.29
Nodes (6): MODIFIED Requirements, Requirement: HTTP server and routing are in an isolated feature module, Scenario: All endpoints respond correctly after refactor, Scenario: CORS headers are present on all responses, Scenario: OPTIONS preflight is handled, Scenario: Unknown path returns 404 JSON

### Community 23 - "Contributor Covenant Code of Conduct"
Cohesion: 0.33
Nodes (5): Attribution, Contributor Covenant Code of Conduct, Enforcement, Our Pledge, Our Standards

### Community 24 - "Requirement: Terminal HTML is a separate file loaded by its feature module"
Cohesion: 0.33
Nodes (5): MODIFIED Requirements, Requirement: Terminal HTML is a separate file loaded by its feature module, Scenario: HTML file is loadable from package, Scenario: /terminal returns valid HTML page, Scenario: Terminal UI is functional in browser

### Community 25 - "feature_request.md"
Cohesion: 0.40
Nodes (4): Additional Context, Alternatives Considered, Problem / Motivation, Proposed Solution

### Community 26 - "PULL_REQUEST_TEMPLATE.md"
Cohesion: 0.50
Nodes (3): Checklist, Related Issue, Summary

## Knowledge Gaps
- **142 isolated node(s):** `basic_usage.sh script`, `Bug Description`, `Steps to Reproduce`, `Expected Behavior`, `Actual Behavior` (+137 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AdminHandler` connect `AdminHandler` to `http_server.py`, `.do_POST`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `create_admin_server()` connect `AdminHandler` to `__main__.py`, `http_server.py`, `test_smoke.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `get_terminal_html()` connect `test_smoke.py` to `http_server.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `AdminHandler` (e.g. with `create_admin_server()` and `TestAdminHandlerClientTimeout`) actually correct?**
  _`AdminHandler` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RodiAdminThreadingServer` (e.g. with `TestAdminHandlerClientTimeout` and `TestAdminServerFactory`) actually correct?**
  _`RodiAdminThreadingServer` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `basic_usage.sh script`, `Bug Description`, `Steps to Reproduce` to the rest of the system?**
  _142 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AdminHandler` be split into smaller, more focused modules?**
  _Cohesion score 0.06553911205073996 - nodes in this community are weakly interconnected._