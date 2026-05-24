## ADDED Requirements

### Requirement: Getting started guide
`docs/getting-started.md` SHALL explain how to download, run, and verify the service in under 5 minutes.

#### Scenario: New user can follow the guide
- **WHEN** user reads `docs/getting-started.md`
- **THEN** they find: prerequisites, one-command install, how to start the server, how to verify it works with `/help`

### Requirement: API reference document
`docs/api-reference.md` SHALL document every HTTP endpoint with method, path, parameters, and a response example.

#### Scenario: Every endpoint is documented
- **WHEN** a developer reads `docs/api-reference.md`
- **THEN** all 10 endpoints are listed: `/help`, `/run` (GET+POST), `/read`, `/ls`, `/find`, `/terminal`, `/session/start`, `/session/send`, `/session/output`, `/session/stop`

### Requirement: Architecture document
`docs/architecture.md` SHALL describe the feature-based module layout with a directory tree and one-sentence description per module.

#### Scenario: Architecture doc matches actual code
- **WHEN** a contributor reads `docs/architecture.md`
- **THEN** the directory tree listed matches the actual file structure in the repository

### Requirement: AI agent usage example
`examples/ai_agent_usage.md` SHALL provide copy-paste HTTP request examples suitable for use by an AI coding agent operating the server.

#### Scenario: AI agent can use examples without modification
- **WHEN** an AI agent reads `examples/ai_agent_usage.md`
- **THEN** it finds working `curl` commands for run, read, session start/send/output/stop
