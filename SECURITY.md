# Security Policy

## Supported Scope

This repository is a research-grade and demonstrative Machine Learning project for ITSM ticket triage. It is not intended to process production secrets, personally identifiable information, or regulated support records.

## Reporting a Vulnerability

Report vulnerabilities privately by opening a confidential security advisory in GitHub, or by contacting the repository maintainer directly before public disclosure.

When reporting an issue, include:

- affected file or component;
- reproduction steps;
- potential impact;
- suggested mitigation, if available.

## Sensitive Data Rules

- Do not commit real tickets, credentials, tokens, or internal asset identifiers.
- Do not store production `.env` files in version control.
- Use only synthetic or sanitized examples in `examples/` and documentation.
- Treat screenshots as public artifacts and avoid exposing real service names, usernames, or support metadata.

## Hardening Expectations

- Keep dependencies pinned when reproducibility matters.
- Review pull requests for accidental exposure of internal data.
- Prefer synthetic datasets for experiments and demonstrations.
