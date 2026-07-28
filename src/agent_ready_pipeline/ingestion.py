"""CSV ingestion utilities."""

from __future__ import annotations

import csv
from pathlib import Path

CsvRow = dict[str, str | None]


class CsvIngestionError(Exception):
    """Base exception for CSV ingestion failures."""


class EmptyCsvError(CsvIngestionError):
    """Raised when a CSV file contains no data rows."""


def load_csv(file_path: str | Path) -> list[CsvRow]:
    """Load a CSV file and return its rows as dictionaries.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A list in which each item represents one CSV row.

    Raises:
        FileNotFoundError: If the provided path does not point to a file.
        EmptyCsvError: If the file has no header or data rows.
        CsvIngestionError: If the file cannot be decoded as UTF-8.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            if reader.fieldnames is None:
                raise EmptyCsvError(f"CSV file has no header: {path}")

            rows = list(reader)

    except UnicodeDecodeError as error:
        raise CsvIngestionError(f"CSV file must use UTF-8 encoding: {path}") from error

    if not rows:
        raise EmptyCsvError(f"CSV file contains no data rows: {path}")

    return rows
