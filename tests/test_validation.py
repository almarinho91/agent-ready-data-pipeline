"""Tests for schema validation."""

from pathlib import Path

import pytest

from agent_ready_pipeline.ingestion import CsvRow, load_csv
from agent_ready_pipeline.validation import (
    EmptyDatasetError,
    InvalidEmailFormatError,
    MissingRequiredColumnsError,
    validate_email_column,
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


def test_validate_email_column_accepts_valid_addresses() -> None:
    """Accept a dataset whose email column holds well-formed addresses."""
    rows: list[CsvRow] = [
        {"id": "1", "email": "ada@example.com"},
        {"id": "2", "email": "grace.hopper@navy.example.org"},
        {"id": "3", "email": "alan+tag@sub.domain.example.co.uk"},
    ]

    validate_email_column(rows)


def test_validate_email_column_rejects_malformed_addresses() -> None:
    """Reject email values that break any formatting rule."""
    rows: list[CsvRow] = [
        {"id": "1", "email": "no-at-sign.example.com"},
        {"id": "2", "email": "two@at@example.com"},
        {"id": "3", "email": "@example.com"},
        {"id": "4", "email": "local@"},
        {"id": "5", "email": "local@nodot"},
        {"id": "6", "email": "spaced address@example.com"},
    ]

    with pytest.raises(
        InvalidEmailFormatError,
        match="Invalid email addresses: 'no-at-sign",
    ) as error_info:
        validate_email_column(rows)

    assert error_info.value.invalid_emails == (
        "no-at-sign.example.com",
        "two@at@example.com",
        "@example.com",
        "local@",
        "local@nodot",
        "spaced address@example.com",
    )


def test_validate_email_column_rejects_missing_values() -> None:
    """Reject ``None`` and empty-string values in the email column."""
    rows: list[CsvRow] = [
        {"id": "1", "email": None},
        {"id": "2", "email": ""},
    ]

    with pytest.raises(
        InvalidEmailFormatError,
        match="Invalid email addresses: None, ''",
    ) as error_info:
        validate_email_column(rows)

    assert error_info.value.invalid_emails == (None, "")


def test_validate_email_column_aggregates_invalid_values_in_row_order() -> None:
    """Aggregate every invalid value while preserving the original row order."""
    rows: list[CsvRow] = [
        {"id": "1", "email": "zoe@example.com"},
        {"id": "2", "email": "zeta@nodot"},
        {"id": "3", "email": None},
        {"id": "4", "email": "abel@example.com"},
        {"id": "5", "email": "alpha.example.com"},
        {"id": "6", "email": ""},
    ]

    with pytest.raises(
        InvalidEmailFormatError,
        match="Invalid email addresses: 'zeta@nodot', None, 'alpha",
    ) as error_info:
        validate_email_column(rows)

    assert error_info.value.invalid_emails == (
        "zeta@nodot",
        None,
        "alpha.example.com",
        "",
    )


def test_validate_email_column_rejects_empty_dataset() -> None:
    """Reject email validation when the dataset contains no rows."""
    with pytest.raises(
        EmptyDatasetError,
        match="Cannot validate an empty dataset",
    ):
        validate_email_column([])


def test_validate_email_column_reports_missing_email_column() -> None:
    """Report a dataset that does not contain the email column."""
    rows: list[CsvRow] = [{"id": "1", "name": "Ada"}]

    with pytest.raises(
        MissingRequiredColumnsError,
        match="Missing required columns: email",
    ) as error_info:
        validate_email_column(rows)

    assert error_info.value.missing_columns == ("email",)


def test_validate_email_column_supports_custom_column_name() -> None:
    """Validate a non-default column when the column name is provided."""
    rows: list[CsvRow] = [
        {"id": "1", "contact": "ada@example.com", "email": "broken"},
        {"id": "2", "contact": "bad-contact", "email": "also-broken"},
    ]

    with pytest.raises(
        InvalidEmailFormatError,
        match="Invalid email addresses: 'bad-contact'",
    ) as error_info:
        validate_email_column(rows, column="contact")

    assert error_info.value.invalid_emails == ("bad-contact",)
