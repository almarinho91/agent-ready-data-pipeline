"""Quality-report generation utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_ready_pipeline.processing import ProcessingResult

QualityReport = dict[str, Any]


def build_quality_report(result: ProcessingResult) -> QualityReport:
    """Build a serializable quality report from a processing result."""
    return {
        "input_rows": result.input_row_count,
        "output_rows": result.output_row_count,
        "duplicate_rows_removed": result.duplicate_rows_removed,
        "missing_values": result.missing_values,
    }


def write_quality_report(
    report: QualityReport,
    output_path: str | Path,
) -> None:
    """Write a quality report to a JSON file.

    Args:
        report: Quality metrics to serialize.
        output_path: Destination path for the JSON report.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
