## MODIFIED Requirements

### Requirement: Command execution is an isolated feature module
The `run_command` function and its `/run` endpoint handler logic SHALL live in `rodi_admin/features/command_execution.py`. The module SHALL export `run_command(cmd_str: str) -> dict` and `handle_run_get(params: dict) -> tuple[int, dict]` and `handle_run_post(body: dict) -> tuple[int, dict]`.

#### Scenario: GET /run?cmd= executes command and returns stdout
- **WHEN** `GET /run?cmd=echo hello` is received
- **THEN** response is `{"success": true, "stdout": "hello\n", "stderr": "", "exit_code": 0}`

#### Scenario: POST /run with JSON body executes command
- **WHEN** `POST /run` is received with body `{"cmd": "uname -a"}`
- **THEN** response contains `success`, `stdout`, `stderr`, `exit_code`

#### Scenario: Command timeout returns error response
- **WHEN** a command runs longer than `COMMAND_TIMEOUT_SECONDS`
- **THEN** response is `{"success": false, "error": "timeout after 30s"}`

#### Scenario: Missing cmd parameter returns 400
- **WHEN** `GET /run` is received with no `cmd` parameter
- **THEN** response status is `400` with `{"error": "Parameter 'cmd' is required"}`
