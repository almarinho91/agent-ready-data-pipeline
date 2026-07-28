"""Tests for CSV ingestion."""

from pathlib import Path

import pytest

from agent_ready_pipeline.ingestion import EmptyCsvError, load_csv


def test_load_csv_returns_rows_as_dictionaries(tmp_path: Path) -> None:
    """Load a valid CSV file and return its rows as dictionaries."""
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "id,name,email\n1,Ana,ana@example.com\n2,Bruno,bruno@example.com\n",
        encoding="utf-8",
    )

    rows = load_csv(csv_path)

    assert rows == [
        {
            "id": "1",
            "name": "Ana",
            "email": "ana@example.com",
        },
        {
            "id": "2",
            "name": "Bruno",
            "email": "bruno@example.com",
        },
    ]


def test_load_csv_raises_error_for_missing_file(tmp_path: Path) -> None:
    """Reject a path that does not point to an existing file."""
    csv_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        load_csv(csv_path)


def test_load_csv_raises_error_when_file_has_no_data_rows(
    tmp_path: Path,
) -> None:
    """Reject a CSV file containing only a header."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("id,name,email\n", encoding="utf-8")

    with pytest.raises(EmptyCsvError, match="contains no data rows"):
        load_csv(csv_path)


def test_load_csv_raises_error_when_file_has_no_header(
    tmp_path: Path,
) -> None:
    """Reject a completely empty CSV file."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")

    with pytest.raises(EmptyCsvError, match="has no header"):
        load_csv(csv_path)
