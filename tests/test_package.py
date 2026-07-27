"""Tests for the package metadata."""

from agent_ready_pipeline import __version__


def test_package_version() -> None:
    """Verify that the package exposes the expected version."""
    assert __version__ == "0.1.0"
