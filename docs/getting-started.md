# Getting Started

## Prerequisites

- Ubuntu 20.04+
- Python 3.10+
- `ufw` installed (`sudo apt install ufw`)
- `sudo` access

## Install

```bash
git clone https://github.com/alishafiee1/rodi-ai-api.git
cd rodi-ai-api
```

No pip install required — stdlib only.

## Start the server

```bash
python3 -m rodi_admin
```

You will be prompted for:
1. **sudo password** — used only to open/close the UFW firewall rule
2. **port** — default is `8889`, press Enter to accept

## Verify it works

```bash
curl http://YOUR_SERVER_IP:8889/help
```

Expected response:
```json
{
  "status": "running",
  "version": "1.0.0",
  ...
}
```

Or open in browser: `http://YOUR_SERVER_IP:8889/terminal`

## Stop the server

Press **Ctrl+C** in the terminal. The firewall rule is removed automatically.

## Configuration via environment variables

```bash
RODI_ADMIN_PORT=9000 python3 -m rodi_admin
```

| Variable | Default | Description |
|---|---|---|
| `RODI_ADMIN_PORT` | `8889` | Suggested port |
| `RODI_ADMIN_MAX_READ_BYTES` | `262144` | Max /read file size |
| `RODI_ADMIN_COMMAND_TIMEOUT` | `30` | /run timeout (seconds) |
