# Security Policy

## Never commit live credentials

Do not commit or open an issue containing:

- SSH passwords or private keys.
- VPS addresses tied to private infrastructure.
- x-ui panel usernames, passwords, paths or API tokens.
- VLESS UUIDs or complete share links.
- Reality private keys, public parameters or Short IDs from a live node.
- Generated Clash YAML files containing live node access parameters.

Store runtime credentials in a Git-ignored local environment file with mode `600`.

## Reporting a vulnerability

Open a GitHub Security Advisory for vulnerabilities in the Skill or scripts. Do not include live server credentials or a production node configuration in a public issue.
