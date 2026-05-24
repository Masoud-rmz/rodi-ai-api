# rodi_admin

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-yellow)
![Platform](https://img.shields.io/badge/platform-Ubuntu%20Linux-orange)
![Build](https://github.com/rodi-ai/rodi-admin-api/actions/workflows/ci.yml/badge.svg)

> A temporary local admin HTTP API for Ubuntu server inspection, command execution, and interactive terminal sessions — designed for AI agent operators and LAN environments.

---

## About

`rodi_admin` opens a short-lived HTTP API on your Ubuntu server so that AI coding agents (or human operators) can run shell commands, read files, list directories, and interact with long-running processes — all over plain HTTP with no dependencies beyond Python 3.10+.

The service automatically opens the chosen port in UFW on startup and removes the rule on exit.

**Intended use:** LAN / private networks only. No authentication by default.

---

## Features

- [x] Run shell commands via `GET /run?cmd=` or `POST /run`
- [x] Read files remotely via `GET /read?path=`
- [x] List directories via `GET /ls?path=`
- [x] Find files via `GET /find?path=&name=&depth=`
- [x] Interactive PTY terminal sessions via `/session/*`
- [x] Browser-based terminal UI at `/terminal`
- [x] Auto-open / auto-close UFW firewall port
- [x] Environment-variable configuration
- [x] Feature-based modular architecture
- [ ] Token-based authentication (planned)
- [ ] Rate limiting (planned)

---

## Requirements

- Python 3.10+
- Ubuntu 20.04+ with `ufw` installed
- `sudo` access (for UFW management)

---

## Installation

```bash
git clone https://github.com/rodi-ai/rodi-admin-api.git
cd rodi-admin-api
```

No external dependencies — uses Python stdlib only.

---

## Usage

```bash
python3 -m rodi_admin
```

Follow the prompts to enter your sudo password and select a port. Then open:

```
http://YOUR_SERVER_IP:8889/help
http://YOUR_SERVER_IP:8889/terminal
```

### CLI options

```bash
python3 -m rodi_admin --help       # User help
python3 -m rodi_admin --help-ai    # AI agent usage guide
```

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `RODI_ADMIN_PORT` | `8889` | Default port to suggest |
| `RODI_ADMIN_MAX_READ_BYTES` | `262144` | Max bytes for /read |
| `RODI_ADMIN_COMMAND_TIMEOUT` | `30` | Command timeout (seconds) |

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/help` | GET | List all endpoints and status |
| `/run?cmd=COMMAND` | GET | Execute a shell command |
| `/run` | POST | Execute a command (JSON body) |
| `/read?path=FILE` | GET | Read a text file |
| `/ls?path=DIR` | GET | List directory contents |
| `/find?path=P&name=N&depth=D` | GET | Find files by name pattern |
| `/terminal` | GET | Browser-based terminal UI |
| `/session/start` | POST | Start an interactive PTY session |
| `/session/send` | POST | Send input to a running session |
| `/session/output?session_id=ID` | GET | Poll session output |
| `/session/stop` | POST | Stop a session |

See [`docs/api-reference.md`](docs/api-reference.md) for full details.

---

## Architecture

```
rodi_admin/
├── __main__.py                 entrypoint
├── config.py                   port, limits, env vars
├── help_texts.py               --help and --help-ai strings
└── features/
    ├── command_execution.py    /run
    ├── file_inspection.py      /read  /ls  /find
    ├── interactive_session.py  /session/*
    ├── firewall.py             UFW open/close
    ├── startup.py              banner, port prompts
    ├── http_server.py          AdminHandler, routing
    └── terminal/
        └── template.html       browser terminal UI
```

See [`docs/architecture.md`](docs/architecture.md) for full documentation.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Security

This tool is designed for **LAN / private environments only**. See [SECURITY.md](SECURITY.md) before deploying.

---

## License

MIT — see [LICENSE](LICENSE).
