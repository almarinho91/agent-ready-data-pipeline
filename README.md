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

## First governed agent run

The repository has completed its first end-to-end governed agent task:

1. `repository-navigator` inspected the codebase and produced an implementation plan.
2. `python-implementer` and `test-engineer` implemented customer email validation.
3. The task evaluator confirmed that only approved files were changed.
4. `code-reviewer` reviewed correctness, typing, tests, architecture, and scope.
5. GitHub Actions validated the change on Python 3.10, 3.11, and 3.12.
6. The change was reviewed and merged through a pull request.

The completed task added:

- `validate_email_column`;
- `InvalidEmailFormatError`;
- aggregation of invalid email values;
- support for custom email-column names;
- tests for valid, malformed, missing, and empty values.

## Current status

The repository now includes a functional data-quality pipeline, automated tests,
continuous integration, repository governance, specialized coding agents, and
a successfully executed task-based agent workflow.

Future work can expand the task-evaluation framework with additional scenarios,
stronger command restrictions, and structured evaluation reports.
