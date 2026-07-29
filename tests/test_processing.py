"""Tests for data cleaning and quality analysis."""

from agent_ready_pipeline.ingestion import CsvRow
from agent_ready_pipeline.processing import (
    count_missing_values,
    process_rows,
    remove_duplicate_rows,
)


def test_count_missing_values_for_each_column() -> None:
    """Count empty, whitespace-only, and null values."""
    rows: list[CsvRow] = [
        {
            "id": "1",
            "name": "Ana",
            "email": "ana@example.com",
        },
        {
            "id": "2",
            "name": "   ",
            "email": None,
        },
        {
            "id": "3",
            "name": "Bruno",
            "email": "",
        },
    ]

    missing_values = count_missing_values(rows)

    assert missing_values == {
        "email": 2,
        "id": 0,
        "name": 1,
    }


def test_remove_duplicate_rows_preserves_original_order() -> None:
    """Remove repeated rows while keeping their first occurrence."""
    first_row: CsvRow = {
        "id": "1",
        "name": "Ana",
        "email": "ana@example.com",
    }
    second_row: CsvRow = {
        "id": "2",
        "name": "Bruno",
        "email": "bruno@example.com",
    }

    rows = [
        first_row,
        second_row,
        first_row.copy(),
    ]

    unique_rows, duplicate_count = remove_duplicate_rows(rows)

    assert unique_rows == [
        first_row,
        second_row,
    ]
    assert duplicate_count == 1


def test_process_rows_returns_cleaned_data_and_metrics() -> None:
    """Return cleaned rows together with data-quality metrics."""
    rows: list[CsvRow] = [
        {
            "id": "1",
            "name": "Ana",
            "email": "ana@example.com",
        },
        {
            "id": "2",
            "name": "Bruno",
            "email": "",
        },
        {
            "id": "2",
            "name": "Bruno",
            "email": "",
        },
    ]

    result = process_rows(rows)

    assert result.cleaned_rows == [
        {
            "id": "1",
            "name": "Ana",
            "email": "ana@example.com",
        },
        {
            "id": "2",
            "name": "Bruno",
            "email": "",
        },
    ]
    assert result.input_row_count == 3
    assert result.output_row_count == 2
    assert result.duplicate_rows_removed == 1
    assert result.missing_values == {
        "email": 1,
        "id": 0,
        "name": 0,
    }
