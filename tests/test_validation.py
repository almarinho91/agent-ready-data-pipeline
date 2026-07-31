"""Tests for schema validation."""

from pathlib import Path

import pytest

from agent_ready_pipeline.ingestion import load_csv
from agent_ready_pipeline.validation import (
    EmptyDatasetError,
    MissingRequiredColumnsError,
    validate_required_columns,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_validate_required_columns_accepts_valid_schema() -> None:
    """Accept a dataset containing every required column."""
    rows = load_csv(FIXTURES_DIR / "valid_customers.csv")

    validate_required_columns(rows, {"id", "name", "email"})


def test_validate_required_columns_reports_missing_columns() -> None:
    """Report required columns that are not present in the dataset."""
    rows = load_csv(FIXTURES_DIR / "missing_columns.csv")

    with pytest.raises(
        MissingRequiredColumnsError,
        match="Missing required columns: country, email",
    ) as error_info:
        validate_required_columns(
            rows,
            {"id", "name", "email", "country"},
        )

    assert error_info.value.missing_columns == ("country", "email")


def test_validate_required_columns_rejects_empty_dataset() -> None:
    """Reject validation when the dataset contains no rows."""
    with pytest.raises(
        EmptyDatasetError,
        match="Cannot validate an empty dataset",
    ):
        validate_required_columns([], {"id", "name", "email"})
