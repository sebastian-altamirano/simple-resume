"""Contains helpers to parse JSON Resume files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

from simple_resume.helpers.validation import validate_resume
from simple_resume.type_definitions.json_resume import JsonResume

if TYPE_CHECKING:
    from simple_resume.type_definitions.json_resume import SimpleResumeMetadata


def get_simple_resume_metadata(resume: JsonResume) -> SimpleResumeMetadata | None:
    """Return the Simple Resume metadata of a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.

    Returns:
        The value of `/meta/simpleResume` if defined, `None` otherwise.
    """
    return resume.get("meta", {}).get("simpleResume")


def read_and_validate_resume(resume_path: str) -> JsonResume:
    """Read and validate a JSON Resume file.

    Args:
        resume_path: The path to the JSON Resume file.

    Returns:
        The content of the JSON Resume file.

    Raises:
        FileNotFoundError: If the file does not exist.
        JSONDecodeError: If the file is not a valid JSON.
        UnsupportedJsonResumeVersionError: If the version of the JSON Resume is not supported.
        InvalidJsonResumeMetadataError: If the metadata of the JSON Resume is not valid.
        InvalidJsonResumeContentError: If the content of the JSON Resume is not valid.
    """
    resume = json.loads(Path(resume_path).resolve().read_text())
    validate_resume(resume)
    return cast(JsonResume, resume)
