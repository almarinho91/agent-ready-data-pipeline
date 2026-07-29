"""Tests for quality-report generation."""

import json
from pathlib import Path

from agent_ready_pipeline.processing import ProcessingResult
from agent_ready_pipeline.reporting import (
    build_quality_report,
    write_quality_report,
)


def test_build_quality_report_returns_serializable_data() -> None:
    """Build a dictionary containing the processing metrics."""
    result = ProcessingResult(
        cleaned_rows=[
            {
                "id": "1",
                "name": "Ana",
                "email": "ana@example.com",
            }
        ],
        input_row_count=2,
        output_row_count=1,
        duplicate_rows_removed=1,
        missing_values={
            "email": 0,
            "id": 0,
            "name": 0,
        },
    )

    report = build_quality_report(result)

    assert report == {
        "input_rows": 2,
        "output_rows": 1,
        "duplicate_rows_removed": 1,
        "missing_values": {
            "email": 0,
            "id": 0,
            "name": 0,
        },
    }


def test_write_quality_report_creates_json_file(
    tmp_path: Path,
) -> None:
    """Write the report as formatted JSON."""
    report = {
        "input_rows": 3,
        "output_rows": 2,
        "duplicate_rows_removed": 1,
        "missing_values": {
            "email": 1,
            "id": 0,
            "name": 0,
        },
    }
    output_path = tmp_path / "reports" / "quality_report.json"

    write_quality_report(report, output_path)

    saved_report = json.loads(output_path.read_text(encoding="utf-8"))

    assert saved_report == report
    assert output_path.is_file()
