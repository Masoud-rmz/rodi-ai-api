# Security Policy

## Scope

`rodi_admin` is designed for **temporary use in LAN or private network environments only**.

- **No authentication** is provided by default
- **All HTTP traffic is unencrypted** (plain HTTP, not HTTPS)
- **Any user on the same network can execute arbitrary shell commands** when the service is running

Do NOT expose this service to the public internet.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not open a public GitHub issue**.

Instead:
1. Open a [GitHub Security Advisory](https://github.com/rodi-ai/rodi-admin-api/security/advisories/new) (private)
2. Describe the vulnerability, steps to reproduce, and potential impact

We will acknowledge reports within 48 hours and aim to release a fix within 7 days for critical issues.

## Security Hardening Tips

- Run only on isolated LAN segments or via SSH tunnel
- Use `ufw` to restrict the port to specific source IPs
- Stop the service immediately after use (Ctrl+C closes the firewall rule automatically)
- Consider wrapping with an SSH tunnel for remote access: `ssh -L 8889:localhost:8889 user@server`
