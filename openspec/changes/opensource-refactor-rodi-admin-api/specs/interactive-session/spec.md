## MODIFIED Requirements

### Requirement: InteractiveSession class is an isolated feature module
`InteractiveSession` and the session registry (`SESSIONS`, `SESSIONS_LOCK`) SHALL live in `rodi_admin/features/interactive_session.py`. The class interface SHALL remain identical.

#### Scenario: Session starts and returns session_id
- **WHEN** `POST /session/start` is received with `{"cmd": "bash"}`
- **THEN** response is `{"success": true, "session_id": "<uuid>", "cmd": "bash"}`

#### Scenario: Session output is pollable
- **WHEN** `GET /session/output?session_id=<id>` is called after session is started
- **THEN** response contains `{"success": true, "output": "...", "running": true}`

#### Scenario: Input can be sent to running session
- **WHEN** `POST /session/send` with `{"session_id": "<id>", "input": "ls\n"}` is received
- **THEN** input is written to the PTY and response is `{"success": true}`

#### Scenario: Session stop cleans up from registry
- **WHEN** `POST /session/stop` with `{"session_id": "<id>"}` is received
- **THEN** session is terminated, removed from SESSIONS dict, response is `{"success": true}`

#### Scenario: Output of unknown session_id returns 404
- **WHEN** `GET /session/output?session_id=unknown-id` is received
- **THEN** response status is `404` with `{"success": false, "error": "Session not found"}`
