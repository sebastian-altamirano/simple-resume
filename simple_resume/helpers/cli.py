"""Contains helpers to parse CLI arguments."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from simple_resume.helpers.constants import DEFAULT_LANGUAGE, DEFAULT_OUTPUT_PATH, DEFAULT_TEMPLATE

if TYPE_CHECKING:
    from simple_resume.type_definitions.json_resume import SimpleResumeMetadata


def get_language(simple_resume_metadata: SimpleResumeMetadata | None, language: str | None) -> str:
    """Return the language of the resume.

    The language is determined in the following order:
    1. From the `language` argument provided to the CLI.
    2. From `/meta/simpleResume/language` in the JSON Resume file.
    3. From the default language.

    Args:
        simple_resume_metadata: The value of `meta/simpleResume` in the JSON Resume file.
        language: The language specified via CLI argument.

    Returns:
        The determined language.
    """
    return (
        language
        or (simple_resume_metadata is not None and simple_resume_metadata.get("language"))
        or DEFAULT_LANGUAGE
    )


def get_output_path(output_path: str | None) -> Path:
    """Resolve the output path or return the default one.

    Args:
        output_path: The output path specified via CLI argument.

    Returns:
        The determined output path.
    """
    return (output_path is not None and Path(output_path).resolve()) or DEFAULT_OUTPUT_PATH


def get_template(simple_resume_metadata: SimpleResumeMetadata | None, template: str | None) -> str:
    """Return the template of the resume.

    The template is determined in the following order:
    1. From the `template` argument provided to the CLI.
    2. From `/meta/simpleResume/template` in the JSON Resume file.
    3. From the default template.

    Args:
        simple_resume_metadata: The value of `meta/simpleResume` in the JSON Resume file.
        template: The template specified via CLI argument.

    Returns:
        The determined template.
    """
    return (
        template
        or (simple_resume_metadata is not None and simple_resume_metadata.get("template"))
        or DEFAULT_TEMPLATE
    )
