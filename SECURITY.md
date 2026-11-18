# Security Policy

## Never commit live credentials

Do not commit or open an issue containing:

- SSH passwords or private keys.
- VPS addresses tied to private infrastructure.
- x-ui panel usernames, passwords, paths or API tokens.
- VLESS UUIDs or complete share links.
- Reality private keys, public parameters or Short IDs from a live node.
- Generated Clash YAML files containing live node access parameters.
- Personal subscription URLs/IDs, QR codes, downloaded subscription files or private panel handoff documents.

Store runtime credentials in a Git-ignored local environment file with mode `600`.

## Reporting a vulnerability

Open a GitHub Security Advisory for vulnerabilities in the Skill or scripts. Do not include live server credentials or a production node configuration in a public issue.

Panel access information is a required private deliverable, not public documentation. Verify HTTPS/login and hand the user a local Git-ignored file with mode `600`; public reports contain only its location and validation result. A shared routing template must contain no per-client proxies or credentials.
