"""Schema-validation utilities."""

from __future__ import annotations

from collections.abc import Collection

from agent_ready_pipeline.ingestion import CsvRow


class SchemaValidationError(ValueError):
    """Base exception for schema-validation failures."""


class EmptyDatasetError(SchemaValidationError):
    """Raised when validation receives an empty dataset."""


class MissingRequiredColumnsError(SchemaValidationError):
    """Raised when required columns are missing from the dataset."""

    def __init__(self, missing_columns: Collection[str]) -> None:
        self.missing_columns = tuple(sorted(missing_columns))

        column_names = ", ".join(self.missing_columns)
        super().__init__(f"Missing required columns: {column_names}")


def validate_required_columns(
    rows: list[CsvRow],
    required_columns: Collection[str],
) -> None:
    """Validate that all required columns are present.

    Args:
        rows: Rows loaded from a CSV file.
        required_columns: Column names that must exist in the dataset.

    Raises:
        EmptyDatasetError: If no rows are provided.
        MissingRequiredColumnsError: If required columns are missing.
    """
    if not rows:
        raise EmptyDatasetError("Cannot validate an empty dataset.")

    available_columns = set(rows[0])
    missing_columns = set(required_columns) - available_columns

    if missing_columns:
        raise MissingRequiredColumnsError(missing_columns)
