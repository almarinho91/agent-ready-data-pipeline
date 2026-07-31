"""Tests for agent-change evaluation."""

from typing import Any

from agent_ready_pipeline.agent_evaluation import evaluate_paths


def create_task(**overrides: Any) -> dict[str, Any]:
    """Create a task specification with optional overrides."""
    task: dict[str, Any] = {
        "allowed_paths": [
            "src/agent_ready_pipeline/validation.py",
            "tests/test_validation.py",
        ],
        "forbidden_paths": [
            ".claude/",
            ".github/",
            "CLAUDE.md",
        ],
        "maximum_changed_files": 2,
        "requires_test_changes": True,
    }
    task.update(overrides)
    return task


def test_evaluate_paths_accepts_changes_within_scope() -> None:
    """Accept production and test changes allowed by the task."""
    changed_files = [
        "src/agent_ready_pipeline/validation.py",
        "tests/test_validation.py",
    ]

    failures = evaluate_paths(changed_files, create_task())

    assert failures == []


def test_evaluate_paths_rejects_file_outside_allowed_scope() -> None:
    """Reject a changed file that is not explicitly allowed."""
    changed_files = [
        "src/agent_ready_pipeline/processing.py",
        "tests/test_validation.py",
    ]

    failures = evaluate_paths(changed_files, create_task())

    assert failures == [
        ("File is outside the allowed scope: src/agent_ready_pipeline/processing.py")
    ]


def test_evaluate_paths_rejects_protected_directory() -> None:
    """Reject changes inside a forbidden directory."""
    changed_files = [
        ".claude/settings.json",
        "tests/test_validation.py",
    ]

    failures = evaluate_paths(changed_files, create_task())

    assert "Forbidden file was modified: .claude/settings.json" in failures
    assert "File is outside the allowed scope: .claude/settings.json" in failures


def test_evaluate_paths_requires_test_changes() -> None:
    """Require a test-file modification when configured by the task."""
    changed_files = [
        "src/agent_ready_pipeline/validation.py",
    ]

    failures = evaluate_paths(changed_files, create_task())

    assert failures == [
        "The task requires a change inside tests/.",
    ]


def test_evaluate_paths_enforces_maximum_file_count() -> None:
    """Reject a change containing more files than the task allows."""
    changed_files = [
        "src/agent_ready_pipeline/validation.py",
        "tests/test_validation.py",
        "tests/test_processing.py",
    ]

    failures = evaluate_paths(
        changed_files,
        create_task(
            allowed_paths=changed_files,
        ),
    )

    assert failures == [
        "Too many files were changed: 3 changed, maximum allowed is 2.",
    ]
