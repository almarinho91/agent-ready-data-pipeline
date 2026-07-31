"""Evaluate repository changes against an agent-task specification."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

TaskSpecification = dict[str, Any]

ALLOWED_COMMANDS: dict[str, tuple[str, ...]] = {
    "ruff format --check .": ("ruff", "format", "--check", "."),
    "ruff check .": ("ruff", "check", "."),
    "mypy src tests": ("mypy", "src", "tests"),
    "mypy src tests scripts": ("mypy", "src", "tests", "scripts"),
    "pytest": ("pytest",),
}


def run_git_command(arguments: list[str]) -> list[str]:
    """Run a Git command and return its non-empty output lines."""
    completed_process = subprocess.run(
        ["git", *arguments],
        check=True,
        capture_output=True,
        text=True,
    )

    return [
        line.strip().replace("\\", "/")
        for line in completed_process.stdout.splitlines()
        if line.strip()
    ]


def get_changed_files() -> list[str]:
    """Return tracked and untracked files changed in the working tree."""
    tracked_files = run_git_command(["diff", "--name-only", "HEAD"])
    untracked_files = run_git_command(["ls-files", "--others", "--exclude-standard"])

    return sorted(set(tracked_files + untracked_files))


def load_task(task_path: Path) -> TaskSpecification:
    """Load and validate an agent-task specification."""
    try:
        task_data = json.loads(task_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Task specification not found: {task_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Task specification is not valid JSON: {task_path}"
        ) from error

    if not isinstance(task_data, dict):
        raise ValueError("Task specification must contain a JSON object.")

    return task_data


def matches_path_rule(file_path: str, rule: str) -> bool:
    """Return whether a file path matches a file or directory rule."""
    normalized_rule = rule.replace("\\", "/")

    if normalized_rule.endswith("/"):
        return file_path.startswith(normalized_rule)

    return file_path == normalized_rule


def evaluate_paths(
    changed_files: list[str],
    task: TaskSpecification,
) -> list[str]:
    """Evaluate changed files against task path restrictions."""
    failures: list[str] = []

    allowed_paths = task.get("allowed_paths", [])
    forbidden_paths = task.get("forbidden_paths", [])
    maximum_changed_files = task.get("maximum_changed_files")

    if not isinstance(allowed_paths, list):
        failures.append("allowed_paths must be a list.")
        allowed_paths = []

    if not isinstance(forbidden_paths, list):
        failures.append("forbidden_paths must be a list.")
        forbidden_paths = []

    if not changed_files:
        failures.append("No repository changes were detected.")
        return failures

    if isinstance(maximum_changed_files, int):
        if len(changed_files) > maximum_changed_files:
            failures.append(
                "Too many files were changed: "
                f"{len(changed_files)} changed, "
                f"maximum allowed is {maximum_changed_files}."
            )

    for file_path in changed_files:
        if any(matches_path_rule(file_path, rule) for rule in forbidden_paths):
            failures.append(f"Forbidden file was modified: {file_path}")

        if allowed_paths and not any(
            matches_path_rule(file_path, rule) for rule in allowed_paths
        ):
            failures.append(f"File is outside the allowed scope: {file_path}")

    if task.get("requires_test_changes") is True:
        test_file_changed = any(
            file_path == "tests" or file_path.startswith("tests/")
            for file_path in changed_files
        )

        if not test_file_changed:
            failures.append("The task requires a change inside tests/.")

    return failures


def run_required_commands(
    task: TaskSpecification,
) -> list[str]:
    """Run allowlisted validation commands required by the task."""
    failures: list[str] = []
    required_commands = task.get("required_commands", [])

    if not isinstance(required_commands, list):
        return ["required_commands must be a list."]

    for command in required_commands:
        if not isinstance(command, str):
            failures.append("Every required command must be a string.")
            continue

        arguments = ALLOWED_COMMANDS.get(command)

        if arguments is None:
            failures.append(f"Command is not allowed: {command}")
            continue

        print(f"\nRunning: {command}")

        completed_process = subprocess.run(
            arguments,
            text=True,
            check=False,
        )

        if completed_process.returncode != 0:
            failures.append(
                f"Command failed with exit code "
                f"{completed_process.returncode}: {command}"
            )

    return failures


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate current repository changes against an agent-task specification."
        )
    )
    parser.add_argument(
        "task",
        type=Path,
        help="Path to the agent-task JSON file.",
    )
    parser.add_argument(
        "--skip-commands",
        action="store_true",
        help="Evaluate changed paths without running quality commands.",
    )

    return parser.parse_args()


def main() -> int:
    """Run the agent-change evaluation."""
    arguments = parse_arguments()

    try:
        task = load_task(arguments.task)
        changed_files = get_changed_files()
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"Evaluation error: {error}", file=sys.stderr)
        return 2

    print("Changed files:")

    for file_path in changed_files:
        print(f"- {file_path}")

    failures = evaluate_paths(changed_files, task)

    if not arguments.skip_commands:
        failures.extend(run_required_commands(task))

    if failures:
        print("\nEvaluation result: FAILED")

        for failure in failures:
            print(f"- {failure}")

        return 1

    print("\nEvaluation result: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
