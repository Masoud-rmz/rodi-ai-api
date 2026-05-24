## MODIFIED Requirements

### Requirement: Firewall management is an isolated feature module
All UFW-related functions (`open_firewall_port`, `cleanup`, `verify_firewall_port_open`, `verify_sudo_password`, `prompt_required_sudo_password`) SHALL live in `rodi_admin/features/firewall.py`. They SHALL use values from `config.py` rather than global variables.

#### Scenario: Port is opened in UFW on startup
- **WHEN** server starts with a valid sudo password
- **THEN** `ufw allow <PORT>/tcp` is executed and verified

#### Scenario: Port is closed in UFW on exit
- **WHEN** process exits (Ctrl+C or normal exit)
- **THEN** `atexit` handler calls `cleanup()` which runs `ufw delete allow <PORT>/tcp`

#### Scenario: Wrong sudo password prompts again
- **WHEN** user enters an incorrect sudo password
- **THEN** verification fails and user is prompted again without exiting

#### Scenario: UFW rule not confirmed causes exit
- **WHEN** `ufw allow` runs successfully but verification check does not find the rule
- **THEN** process exits with code 1 and an error message is printed
