# Contributing to rodi_admin

Thank you for your interest in contributing!

## Setup

```bash
git clone https://github.com/alishafiee1/rodi-ai-api.git
cd rodi-ai-api
python3 -m venv .venv && source .venv/bin/activate
pip install pytest
```

## Running tests

```bash
# Import smoke test (no sudo required)
RODI_SMOKE_TEST=1 python3 -m pytest tests/ -v
```

## Code style

- PEP 8 formatting
- Type hints on all functions
- Docstrings on all public functions (purpose --- description format)
- Max 100 lines per file — split into a new module if needed
- No external dependencies (stdlib only)

## Pull request process

1. Fork the repo and create a feature branch: `git checkout -b feature/my-change`
2. Make your changes following the code style above
3. Run tests and verify they pass
4. Open a PR against `main` — fill in the PR template checklist
5. Maintainers will review within a few days

## Feature requests

Open an issue using the Feature Request template before starting large changes.

## Questions?

- GitHub [Issues](https://github.com/alishafiee1/rodi-ai-api/issues)
- Email: alishafiee1@gmail.com
- Telegram: [@aliaghashafiee](https://t.me/aliaghashafiee)
