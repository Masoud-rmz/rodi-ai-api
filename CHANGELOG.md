# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-05-24

### Added
- Initial public release on GitHub
- Feature-based modular package `rodi_admin/` replacing single-file `api_admin.py`
- `python3 -m rodi_admin` entrypoint
- Centralized `config.py` with environment variable overrides
- `features/terminal/template.html` — HTML template extracted from Python source
- `tests/test_smoke.py` — opt-in smoke tests (`RODI_SMOKE_TEST=1`)
- GitHub community files: README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- GitHub Actions CI workflow
- `docs/` directory: getting-started, api-reference, architecture
- `examples/` directory: basic_usage, ai_agent_usage

### Changed
- `api_admin.py` is now a deprecated shim — prints deprecation notice and delegates to `rodi_admin`

### Deprecated
- `api_admin.py` direct invocation — will be removed in v2.0

---

## [Unreleased]

### Planned
- Token-based authentication
- Rate limiting
- HTTPS support via self-signed cert option
