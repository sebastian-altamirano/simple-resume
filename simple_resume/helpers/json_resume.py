"""Contains helpers to parse JSON Resume files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from simple_resume.helpers.cli_logging import (
    print_error_message,
    print_info_message,
    print_success_message,
)
from simple_resume.models.json_resume import JsonResume
from simple_resume.type_definitions.cli import SimpleResumeMetadataCliOverrides


def _apply_cli_overrides(
    resume: dict[str, Any], cli_overrides: SimpleResumeMetadataCliOverrides
) -> None:
    simple_resume_metadata = resume.setdefault("meta", {}).setdefault("simpleResume", {})
    if cli_overrides["language"]:
        simple_resume_metadata["language"] = cli_overrides["language"]
    if cli_overrides["template"]:
        simple_resume_metadata.setdefault("template", {})["name"] = cli_overrides["template"]


def read_and_validate_resume(
    resume_path: str, cli_overrides: SimpleResumeMetadataCliOverrides | None = None
) -> JsonResume:
    """Read and validate a JSON Resume file.

    Args:
        resume_path: The path to the JSON Resume file.
        cli_overrides: CLI options that override the resume metadata.

    Returns:
        The content of the JSON Resume file.

    Raises:
        FileNotFoundError: If the file does not exist.
        JSONDecodeError: If the file is not a valid JSON.
        ValidationError: If the resume is not valid.
    """
    resume = cast(
        dict[str, Any], json.loads(Path(resume_path).resolve().read_text(encoding="utf-8"))
    )
    print_info_message("Validating the resume...")

    try:
        if cli_overrides:
            _apply_cli_overrides(resume, cli_overrides)

        validated_resume = JsonResume(**resume)
    except:
        print_error_message("The resume is not valid.")
        raise

    print_success_message("The resume is valid.")
    return validated_resume
