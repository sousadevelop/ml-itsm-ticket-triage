# Contributing Guide

## Contribution Principles

This repository accepts contributions focused on reproducibility, documentation quality, ML evaluation quality, and safe demo-ready ITSM workflows.

## Before Opening a Pull Request

- keep examples synthetic and sanitized;
- avoid committing secrets, proprietary tickets, or customer data;
- preserve existing notebooks and experimental artifacts unless the change explicitly targets them;
- document any model or dataset assumption that changes classification behavior.

## Recommended Workflow

1. Create a feature branch from `main`.
2. Make focused changes with clear commit messages.
3. Re-run the training pipeline if model behavior changes.
4. Validate the Streamlit app locally before requesting review.
5. Update documentation when architecture, inference behavior, or deployment instructions change.

## Code Style

- Prefer clear, small Python modules.
- Keep the ML pipeline deterministic when possible.
- Use synthetic tickets and stable examples for tests and docs.
- Do not introduce unnecessary dependencies.

## Pull Request Checklist

- [ ] Documentation updated
- [ ] No secrets or real support data included
- [ ] Model artifact regenerated when training logic changed
- [ ] Example inputs and outputs still match the current interface
- [ ] README and translated docs remain structurally aligned
