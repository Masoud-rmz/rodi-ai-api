## ADDED Requirements

### Requirement: Feature-based package layout
The codebase SHALL be organized as a Python package `rodi_admin/` with one module per feature inside `features/`. Each feature module SHALL be independently importable and contain only the logic for its domain.

#### Scenario: Package is runnable as a module
- **WHEN** user runs `python3 -m rodi_admin`
- **THEN** the server starts identically to `python3 api_admin.py`

#### Scenario: Each feature is an independent module
- **WHEN** a developer imports `from rodi_admin.features.command_execution import run_command`
- **THEN** it succeeds without importing unrelated features

#### Scenario: HTML template is a separate file
- **WHEN** the `terminal` feature is loaded
- **THEN** it reads `template.html` from its own directory using `Path(__file__).parent`

### Requirement: Backward-compatible shim
The original `api_admin.py` SHALL remain in the repository root and SHALL delegate to `rodi_admin.__main__` with a visible deprecation notice printed to stdout.

#### Scenario: Old invocation still works
- **WHEN** user runs `python3 api_admin.py`
- **THEN** server starts normally and a deprecation message is printed: "Note: api_admin.py is deprecated. Use: python3 -m rodi_admin"
