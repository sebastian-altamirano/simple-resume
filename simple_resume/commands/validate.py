"""Contains the logic of the `validate` command."""

from __future__ import annotations

from simple_resume.helpers.json_resume import read_and_validate_resume
from simple_resume.type_definitions.cli import (  # noqa: TCH001 Typer requires these type annotations to be available at runtime.
    ResumePath,
)


def validate(resume_path: ResumePath) -> None:
    """Validate a JSON resume."""
    read_and_validate_resume(resume_path)
