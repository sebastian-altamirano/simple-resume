"""Contains helpers to validate JSON Resume files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from jsonschema import ValidationError, validate

from simple_resume.helpers.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_TEMPLATE,
    JSON_RESUME_SCHEMA_PATH,
    JSON_RESUME_SCHEMA_URL,
    SIMPLE_RESUME_METADATA_SCHEMA_PATH,
)
from simple_resume.helpers.exceptions import (
    InvalidJsonResumeContentError,
    InvalidJsonResumeMetadataError,
    UnsupportedJsonResumeVersionError,
)
from simple_resume.helpers.i18n import get_supported_languages
from simple_resume.helpers.logging import print_info_message
from simple_resume.helpers.templates import get_registered_templates
from simple_resume.type_definitions.json_resume import SimpleResumeMetadata


def validate_resume(resume: dict[str, Any]) -> None:
    """Validate a JSON resume.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        UnsupportedJsonResumeVersionError: If the version of the JSON Resume is not supported.
        InvalidJsonResumeMetadataError: If the metadata of the JSON Resume is not valid.
        InvalidJsonResumeContentError: If the content of the JSON Resume is not valid.
    """
    _validate_resume_version(resume)
    _validate_resume_metadata(resume)
    _validate_resume_content(resume)


def _validate_resume_content(resume: dict[str, Any]) -> None:
    """Validate the content of a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        InvalidJsonResumeContentError: If the content of the JSON Resume is not valid.
    """
    try:
        validate(
            instance=resume,
            schema=json.load(Path.open(JSON_RESUME_SCHEMA_PATH, encoding="utf-8")),
        )
    except ValidationError as error:
        raise InvalidJsonResumeContentError() from error


def _validate_resume_metadata(resume: dict[str, Any]) -> None:
    """Validate the metadata of a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        InvalidJsonResumeMetadataError: If the metadata of the JSON Resume is not valid.
    """
    if "meta" not in resume or "simpleResume" not in resume["meta"]:
        return

    metadata = resume["meta"]["simpleResume"]
    try:
        validate(
            instance=metadata,
            schema=json.load(Path.open(SIMPLE_RESUME_METADATA_SCHEMA_PATH, encoding="utf-8")),
        )
    except ValidationError as error:
        raise InvalidJsonResumeMetadataError() from error
    metadata = cast(SimpleResumeMetadata, metadata)

    if (language := metadata.get("language")) is None:
        print_info_message(
            "No language is specified in the resume metadata, the default language "
            f"({DEFAULT_LANGUAGE}) will be used when exporting or serving the resume."
        )
    elif language not in (supported_languages := get_supported_languages()):
        error_message = (
            f"The language '{language}' is not supported, the supported languages are: "
            f"{supported_languages}."
        )
        raise InvalidJsonResumeMetadataError(error_message)

    if (template := metadata.get("template")) is None:
        print_info_message(
            "No template is specified in the resume metadata, the default template "
            f"({DEFAULT_TEMPLATE}) will be used when exporting or serving the resume."
        )
    elif template not in (registered_templates := get_registered_templates()):
        error_message = (
            f"The template '{template}' does not exist, the registered templates are: "
            f"{registered_templates}."
        )
        raise InvalidJsonResumeMetadataError(error_message)


def _validate_resume_version(resume: dict[str, Any]) -> None:
    """Validate if the version of a JSON Resume is supported.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        UnsupportedJsonResumeVersionError: If the version of the JSON Resume is not supported.
    """
    if (schema_url := resume.get("$schema")) and schema_url != JSON_RESUME_SCHEMA_URL:
        raise UnsupportedJsonResumeVersionError(schema_url)
