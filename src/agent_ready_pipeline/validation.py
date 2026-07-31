"""Schema-validation utilities."""

from __future__ import annotations

from collections.abc import Collection, Sequence

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


class InvalidEmailFormatError(SchemaValidationError):
    """Raised when a dataset contains malformed email addresses."""

    def __init__(self, invalid_emails: Sequence[str | None]) -> None:
        self.invalid_emails = tuple(invalid_emails)

        values = ", ".join(repr(value) for value in self.invalid_emails)
        super().__init__(f"Invalid email addresses: {values}")


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


def _is_valid_email(value: str | None) -> bool:
    """Return whether a value satisfies the conservative email rule.

    Args:
        value: Candidate email value.

    Returns:
        True if the value is a well-formed email address.
    """
    if not value:
        return False

    if any(character.isspace() for character in value):
        return False

    if value.count("@") != 1:
        return False

    local_part, _, domain = value.partition("@")

    if not local_part or not domain:
        return False

    return "." in domain


def validate_email_column(
    rows: list[CsvRow],
    column: str = "email",
) -> None:
    """Validate that every row contains a well-formed email address.

    A value is considered valid only when all of the following hold:

    - it is a non-empty string (``None`` and ``""`` are invalid);
    - it contains exactly one ``"@"`` character;
    - the local part before ``"@"`` is non-empty;
    - the domain after ``"@"`` is non-empty;
    - the domain contains at least one ``"."``;
    - the value contains no whitespace characters.

    All invalid values are collected before a single error is raised.

    Args:
        rows: Rows loaded from a CSV file.
        column: Name of the column holding email addresses.

    Raises:
        EmptyDatasetError: If no rows are provided.
        MissingRequiredColumnsError: If the email column is missing.
        InvalidEmailFormatError: If any row holds a malformed email address.
    """
    validate_required_columns(rows, [column])

    invalid_emails = [
        row.get(column) for row in rows if not _is_valid_email(row.get(column))
    ]

    if invalid_emails:
        raise InvalidEmailFormatError(invalid_emails)
