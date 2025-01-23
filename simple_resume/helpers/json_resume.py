"""Contains helpers to parse JSON Resume files."""

from __future__ import annotations

import json
from pathlib import Path

from simple_resume.helpers.cli_logging import (
    print_error_message,
    print_info_message,
    print_success_message,
)
from simple_resume.models.json_resume import JsonResume


def read_and_validate_resume(resume_path: str) -> JsonResume:
    """Read and validate a JSON Resume file.

    Args:
        resume_path: The path to the JSON Resume file.

    Returns:
        The content of the JSON Resume file.

    Raises:
        FileNotFoundError: If the file does not exist.
        JSONDecodeError: If the file is not a valid JSON.
        ValidationError: If the resume is not valid.
    """
    resume = json.loads(Path(resume_path).resolve().read_text())

    print_info_message("Validating the resume...")

    try:
        validated_resume = JsonResume(**resume)
    except:
        print_error_message("The resume is not valid.")
        raise

    print_success_message("The resume is valid.")
    return validated_resume
