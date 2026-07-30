# Architecture

## Overview

Agent-Ready Data Pipeline is a small Python application for validating,
cleaning, and analyzing CSV datasets.

The codebase follows a modular structure in which each module has one primary
responsibility.

## Data flow

```text
CSV file
    |
    v
Ingestion
    |
    v
Schema validation
    |
    v
Data processing
    |
    v
Quality report

## Package structure

```bash
ingestion.py
```

Responsible for reading external CSV files.

This module:

- verifies that the input file exists;
- reads CSV rows as dictionaries;
- handles empty files;
- handles unsupported text encoding.

It must not perform data cleaning or business-rule validation.

```bash
validation.py
```

Responsible for validating dataset structure and business requirements.

This module currently:

- verifies that datasets contain rows;
- checks that required columns are present.

It must not read or write files.

```bash
processing.py
```

Responsible for pure data-cleaning and quality-analysis operations.

This module currently:

- removes duplicate rows;
- counts missing values;
- calculates input and output row metrics.

Processing functions should not access the file system.

```bash
reporting.py
```

Responsible for converting processing results into serializable reports and
writing those reports to disk.

This module:

- builds the quality-report structure;
- writes formatted JSON files;
- creates missing output directories when necessary.

```bash
__init__.py
```

Defines package-level metadata such as the current version.

## Tests

Tests are located in the ```tests/ ``` directory and follow the structure of the
production modules.

```bash
tests/
    test_package.py
    test_ingestion.py
    test_validation.py
    test_processing.py
    test_reporting.py
```
Tests should:

- cover both successful and failing behavior;
- use temporary files instead of writing into the repository;
- remain independent from one another;
- include a regression test for every bug fix.

## Dependency direction

The intended dependency flow is:

```bash
reporting -> processing -> ingestion
validation -------------> ingestion
```

Lower-level modules must not import higher-level modules.

For example:

- ```ingestion.py``` must not import ```processing.py```;
- ```processing.py``` must not import ```reporting.py```;
- ```validation.py``` must not write reports.

## Quality requirements

Every change must pass:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
```

## Planned extensions

The initial release will later include:

- a command-line interface;
- repository instructions for AI coding agents;
- automated continuous integration;
- task-based evaluation of agent-generated changes.