# Agent-Ready Data Pipeline

A Python reference project demonstrating how a real data-processing application
can be structured for safe and governed AI-assisted software development.

The project combines a CSV data-quality pipeline with repository instructions,
specialized coding agents, automated quality checks, and task-based evaluation
of agent-generated changes.

## Features

- CSV ingestion using the Python standard library
- Required-column schema validation
- Duplicate-row removal
- Missing-value analysis
- Structured JSON quality reports
- Automated tests with pytest
- Formatting and linting with Ruff
- Static type checking with mypy
- Multi-version CI with GitHub Actions
- Repository governance through `CLAUDE.md`
- Specialized Claude Code agents
- Task-based evaluation of repository changes

## Data-quality workflow

```text
CSV input
    -> ingestion
    -> schema validation
    -> data cleaning
    -> quality analysis
    -> JSON report
```

## Project structure

```text
agent-ready-data-pipeline/
├── .claude/
│   ├── agents/
│   └── settings.json
├── .github/
│   └── workflows/
├── evals/
│   └── tasks/
├── scripts/
├── src/
│   └── agent_ready_pipeline/
├── tests/
├── ARCHITECTURE.md
├── CLAUDE.md
├── pyproject.toml
└── README.md
```

## Development setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install the project and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the complete local quality suite:

```bash
ruff format --check .
ruff check .
mypy src tests scripts
pytest
```

## Repository governance

The repository contains a root-level `CLAUDE.md` file defining:

- architectural boundaries;
- coding and testing requirements;
- protected files;
- required validation commands;
- task-completion criteria.

The `.claude/settings.json` file defines scoped permissions for repository-level
agent activity.

## Specialized agents

The project currently includes:

- `repository-navigator`: explores the codebase and produces implementation plans;
- `python-implementer`: implements focused Python changes;
- `test-engineer`: creates and updates tests;
- `code-reviewer`: reviews repository changes without modifying files.

## Agent-change evaluation

Agent tasks are described as JSON specifications under:

```text
evals/tasks/
```

A task can define:

- allowed paths;
- forbidden paths;
- maximum changed files;
- required test modifications;
- required quality commands.

Run an evaluation with:

```bash
python scripts/evaluate_agent_change.py \
  evals/tasks/add-email-validation.json
```

The evaluator checks the current Git working-tree changes against the selected
task specification.

## Continuous integration

GitHub Actions runs the complete quality suite on:

- Python 3.10
- Python 3.11
- Python 3.12

The workflow is triggered for pushes and pull requests targeting `main`.

## Current status

The initial repository architecture, data-quality modules, agent governance,
continuous integration, and change-evaluation framework are implemented.

The next development step is to execute the first governed agent task and
evaluate the resulting repository changes.
