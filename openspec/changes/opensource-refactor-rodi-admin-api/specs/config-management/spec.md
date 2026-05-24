## ADDED Requirements

### Requirement: Centralized config module
All configurable constants SHALL live in `rodi_admin/config.py`. Feature modules SHALL import from `config.py` and SHALL NOT define their own magic numbers.

#### Scenario: Default config works without environment variables
- **WHEN** `rodi_admin` starts with no environment variables set
- **THEN** port defaults to `8889`, `MAX_READ_BYTES` defaults to `262144`, `COMMAND_TIMEOUT_SECONDS` defaults to `30`

### Requirement: Environment variable overrides
Each config value SHALL be overridable via environment variable without code changes.

#### Scenario: Port overridden via environment variable
- **WHEN** user sets `RODI_ADMIN_PORT=9000` before running
- **THEN** server starts on port 9000 (before the interactive prompt, or as the prompt default)

#### Scenario: Invalid env var value falls back to default
- **WHEN** user sets `RODI_ADMIN_PORT=not_a_number`
- **THEN** server uses default port `8889` and prints a warning to stderr
