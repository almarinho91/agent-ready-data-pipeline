"""Data-cleaning and quality-analysis utilities."""

from __future__ import annotations

from dataclasses import dataclass

from agent_ready_pipeline.ingestion import CsvRow


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    """Results produced by the data-cleaning workflow."""

    cleaned_rows: list[CsvRow]
    input_row_count: int
    output_row_count: int
    duplicate_rows_removed: int
    missing_values: dict[str, int]


def _is_missing(value: str | None) -> bool:
    """Return whether a CSV value should be considered missing."""
    return value is None or value.strip() == ""


def count_missing_values(rows: list[CsvRow]) -> dict[str, int]:
    """Count missing values for every column in the dataset."""
    columns = {column for row in rows for column in row}

    return {
        column: sum(1 for row in rows if _is_missing(row.get(column)))
        for column in sorted(columns)
    }


def _row_signature(
    row: CsvRow,
) -> tuple[tuple[str, str | None], ...]:
    """Create a hashable representation of a CSV row."""
    return tuple(sorted(row.items()))


def remove_duplicate_rows(
    rows: list[CsvRow],
) -> tuple[list[CsvRow], int]:
    """Remove duplicate rows while preserving their original order."""
    seen_rows: set[tuple[tuple[str, str | None], ...]] = set()
    unique_rows: list[CsvRow] = []

    for row in rows:
        signature = _row_signature(row)

        if signature in seen_rows:
            continue

        seen_rows.add(signature)
        unique_rows.append(row.copy())

    duplicate_count = len(rows) - len(unique_rows)

    return unique_rows, duplicate_count


def process_rows(rows: list[CsvRow]) -> ProcessingResult:
    """Clean CSV rows and calculate data-quality metrics."""
    cleaned_rows, duplicate_rows_removed = remove_duplicate_rows(rows)
    missing_values = count_missing_values(cleaned_rows)

    return ProcessingResult(
        cleaned_rows=cleaned_rows,
        input_row_count=len(rows),
        output_row_count=len(cleaned_rows),
        duplicate_rows_removed=duplicate_rows_removed,
        missing_values=missing_values,
    )
