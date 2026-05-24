# Architecture

`rodi_admin` uses a feature-based module layout. Each file owns exactly one domain concern.

## Directory Tree

```
rodi_admin/
├── __init__.py                  package metadata and version
├── __main__.py                  CLI entrypoint (python3 -m rodi_admin)
├── config.py                    PORT, limits — reads env vars
├── help_texts.py                --help and --help-ai string constants
└── features/
    ├── __init__.py
    ├── command_execution.py     run_command() + /run GET/POST handlers
    ├── file_inspection.py       safe_read_text_file() + /read /ls /find handlers
    ├── interactive_session.py   InteractiveSession class + /session/* handlers
    ├── firewall.py              UFW open/close, sudo password verification
    ├── startup.py               port prompts, banner, local IP detection
    ├── http_server.py           AdminHandler routing + start_server()
    └── terminal/
        ├── __init__.py          get_terminal_html() loader
        └── template.html        browser terminal UI (HTML + JS)

tests/
└── test_smoke.py                opt-in tests (RODI_SMOKE_TEST=1)

docs/
├── getting-started.md
├── api-reference.md
└── architecture.md              (this file)

examples/
├── basic_usage.sh               curl examples
└── ai_agent_usage.md            guide for AI coding agents

.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
├── PULL_REQUEST_TEMPLATE.md
└── workflows/
    └── ci.yml                   GitHub Actions CI
```

## Data Flow

```
python3 -m rodi_admin
    └── __main__.main()
            ├── firewall.prompt_required_sudo_password()
            ├── startup.prompt_available_port()
            ├── firewall.open_firewall_port()
            ├── startup.print_startup_banner()
            └── http_server.start_server()
                    └── AdminHandler
                            ├── do_GET  → command_execution / file_inspection /
                            │             interactive_session / terminal
                            ├── do_POST → command_execution / interactive_session
                            └── do_OPTIONS → CORS preflight
```
