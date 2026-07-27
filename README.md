# Agent-Ready Data Pipeline

A Python reference project demonstrating how clear repository structure,
automated quality checks, and explicit development rules can support safe
AI-assisted software development.

## Project status

This project is currently under active development.

## Goals

- Build a small and testable CSV data-quality pipeline.
- Separate ingestion, validation, processing, and reporting responsibilities.
- Define clear repository instructions for AI coding agents.
- Enforce code-quality requirements through automated checks.
- Evaluate agent-generated changes against repository policies.

## Planned workflow

```text
CSV input
    -> schema validation
    -> data cleaning
    -> JSON quality report
```

## Development setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the quality checks:

```bash
ruff format --check .
ruff check .
mypy src
pytest
```
## Roadmap

- CSV ingestion and schema validation
- Data cleaning and quality reporting
- Automated tests
- Repository governance for AI coding agents
- Continuous integration
- Agent-change evaluation
