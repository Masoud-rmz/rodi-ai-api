# GitHub Repository Setup Checklist

Manual steps to complete after pushing documentation updates to [alishafiee1/rodi-ai-api](https://github.com/alishafiee1/rodi-ai-api).

## About (repository homepage)

Go to [Settings](https://github.com/alishafiee1/rodi-ai-api/settings) or click the gear icon next to **About** on the repo page.

- [ ] **Description:**
  ```
  Give AI agents a simple HTTP bridge to your Ubuntu server — run commands, read configs, install packages, and manage interactive sessions without memorizing every Linux command.
  ```
- [ ] **Website:** leave empty (standalone project)
- [ ] **Topics:** add all of these:
  - `ubuntu-ai-agent`
  - `linux-ai-agent`
  - `perplexity-agent`
  - `web-terminal`
  - `ai-terminal`
  - `python`
  - `ubuntu`
  - `admin-api`
  - `http-api`
  - `server-management`
  - `ai-agent`

## CI Badge

The README badge points to:
```
https://github.com/alishafiee1/rodi-ai-api/actions/workflows/ci.yml/badge.svg
```

- [ ] Push code to `main` — GitHub Actions runs automatically
- [ ] Check [Actions tab](https://github.com/alishafiee1/rodi-ai-api/actions) — badge turns green when tests pass
- [ ] If badge shows "unknown" before first run, that is normal

## Release v1.0.0

Go to [Releases](https://github.com/alishafiee1/rodi-ai-api/releases) → **Draft a new release**

- [ ] **Tag:** `v1.0.0`
- [ ] **Target:** `main`
- [ ] **Title:** `v1.0.0 — Initial public release`
- [ ] **Release notes:** copy from [CHANGELOG.md](../CHANGELOG.md) section `[1.0.0] - 2026-05-24`
- [ ] Publish release

## Security

Go to [Security](https://github.com/alishafiee1/rodi-ai-api/security) tab

- [ ] Enable **Private vulnerability reporting** (if not already enabled)
- [ ] Verify [SECURITY.md](../SECURITY.md) link works from repo Security policy

## Screenshots

- [ ] Add PNG files to [docs/images/](images/) per [docs/images/README.md](images/README.md)
- [ ] Commit and push — README gallery will show images

## Support channels (already in docs)

| Channel | Contact |
|---------|---------|
| GitHub Issues | https://github.com/alishafiee1/rodi-ai-api/issues |
| Email | alishafiee1@gmail.com |
| Telegram | @aliaghashafiee |
