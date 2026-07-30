# Project Instructions

@ARCHITECTURE.md

## Project purpose

This repository contains a Python data-quality pipeline that reads, validates,
cleans, and analyzes CSV datasets.

The repository also demonstrates how explicit instructions and automated quality
checks can support safe AI-assisted software development.

## Development environment

- Python 3.10 or later
- Source code under `src/agent_ready_pipeline/`
- Tests under `tests/`
- Package installed in editable mode with development dependencies

Install the project with:

```bash
python -m pip install -e ".[dev]"
```

## Required development workflow

Before making a change:

1. Read the relevant production module and its tests.
2. Identify the smallest set of files required for the task.
3. Check the architectural responsibilities in `ARCHITECTURE.md`.
4. Avoid unrelated refactoring.

While making a change:

1. Preserve existing public behavior unless the task explicitly changes it.
2. Keep each module within its documented responsibility.
3. Add or update tests for every behavioral change.
4. Use clear names, type hints, and focused functions.

Before completing a change, run:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
```

## Coding rules

- Use Python 3.10-compatible syntax.
- Add type hints to public functions and methods.
- Add concise docstrings to public classes and functions.
- Prefer the Python standard library when it provides a clear solution.
- Use specific exceptions with actionable error messages.
- Do not silently ignore invalid input.
- Do not mutate input data unless the function explicitly documents it.
- Avoid adding dependencies without a clear requirement.

## Architectural boundaries

- File reading belongs in `ingestion.py`.
- Schema and business-rule checks belong in `validation.py`.
- Pure cleaning and analysis belong in `processing.py`.
- Report construction and file output belong in `reporting.py`.
- Tests must remain outside the production package.
- Lower-level modules must not import higher-level modules.

## Testing rules

- Test successful and failing behavior.
- Use `tmp_path` for temporary files.
- Keep tests deterministic and independent.
- Every bug fix must include a regression test.
- Assert observable behavior rather than internal implementation details.

## Repository safety

Unless the task explicitly requires it:

- Do not modify `CLAUDE.md` or `ARCHITECTURE.md`.
- Do not modify GitHub workflow or security configuration.
- Do not access `.env`, credential, token, or secret files.
- Do not run destructive file-system commands.
- Do not push commits or rewrite Git history.
- Do not make broad changes outside the requested scope.

## Definition of done

A task is complete only when:

1. The requested behavior is implemented.
2. Relevant tests have been added or updated.
3. Formatting, linting, type checking, and tests pass.
4. Architectural boundaries are respected.
5. The diff contains no unrelated changes.
6. Documentation is updated when public behavior or architecture changes.
