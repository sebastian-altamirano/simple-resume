"""Contains helpers to validate JSON Resume files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from jsonschema import ValidationError, validate

from simple_resume.helpers.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_TEMPLATE,
    JSON_RESUME_SCHEMA_PATH,
    JSON_RESUME_SCHEMA_URL,
    SIMPLE_RESUME_METADATA_SCHEMA_PATH,
)
from simple_resume.helpers.dates import get_current_date, parse_date
from simple_resume.helpers.exceptions import (
    EndDateBeforeStartDateError,
    FutureDateError,
    InvalidJsonResumeContentError,
    InvalidJsonResumeMetadataError,
    UnsupportedJsonResumeVersionError,
)
from simple_resume.helpers.i18n import get_supported_languages
from simple_resume.helpers.logging import (
    print_error_message,
    print_info_message,
    print_success_message,
    print_warning_message,
)
from simple_resume.helpers.templates import get_registered_templates

if TYPE_CHECKING:
    from simple_resume.type_definitions.json_resume import JsonResume


def validate_resume(resume: JsonResume) -> None:
    """Validate a JSON resume.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        UnsupportedJsonResumeVersionError: If the version of the JSON Resume is not supported.
        InvalidJsonResumeMetadataError: If the metadata of the JSON Resume is not valid.
        InvalidJsonResumeContentError: If the content of the JSON Resume is not valid.
    """
    print_info_message("Validating the resume...")

    try:
        _validate_resume_version(resume)
        _validate_resume_metadata(resume)
        _validate_resume_content(resume)
        _validate_resume_dates(resume)
    except:
        print_error_message("The resume is not valid.")
        raise

    print_success_message("The resume is valid.")


def _validate_resume_content(resume: JsonResume) -> None:
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


def _validate_resume_date(date_json_pointer: str, date: str | None) -> None:
    """Validate a date of a JSON Resume.

    Note: The date is converted to the local timezone before validation.

    Args:
        date_json_pointer: The JSON Pointer to the date, e.g. `/certificates/0/date`.
        date: The date, or `None` if not provided.

    Raises:
        FutureDateError: If the date is in the future.
    """
    if not date:
        return

    parsed_date = parse_date(date)
    if parsed_date > get_current_date():
        raise FutureDateError(date_json_pointer, date)


def _validate_resume_date_range(
    start_date_json_pointer: str,
    end_date_json_pointer: str,
    start_date: str | None,
    end_date: str | None,
) -> None:
    """Validate a start date and an end date of a JSON Resume.

    Note: Both dates are converted to the local timezone before validation.

    Args:
        start_date_json_pointer: The JSON Pointer to the start date, e.g. `/work/0/startDate`.
        end_date_json_pointer: The JSON Pointer to the end date, e.g. `/work/0/endDate`.
        start_date: The start date, or `None` if not provided.
        end_date: The end date, or `None` if not provided.

    Raises:
        EndDateBeforeStartDateError: If the end date is before the start date.
        FutureDateError: If the start date is in the future.
    """
    if not start_date:
        return

    parsed_start_date = parse_date(start_date)
    if parsed_start_date > get_current_date():
        raise FutureDateError(start_date_json_pointer, start_date)

    if not end_date:
        return

    parsed_end_date = parse_date(end_date)
    if parsed_end_date < parsed_start_date:
        raise EndDateBeforeStartDateError(
            start_date_json_pointer, end_date_json_pointer, start_date, end_date
        )


def _validate_resume_dates(resume: JsonResume) -> None:
    """Validate the dates of a JSON Resume.

    Note: All dates are converted to the local timezone before validation.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        EndDateBeforeStartDateError: If an end date is before a start date.
        FutureDateError: If a date is in the future.
    """
    keys_with_date_range = ("work", "volunteer", "projects", "education")
    for key in keys_with_date_range:
        entries = resume.get(key, [])
        for index, item in enumerate(entries):
            _validate_resume_date_range(
                f"/{key}/{index}/startDate",
                f"/{key}/{index}/endDate",
                item.get("startDate", None),
                item.get("endDate", None),
            )

    # `publications` is not included because `/publications/{index}/releaseDate` may be in the
    # future.
    keys_with_date = ("awards", "certificates")
    for key in keys_with_date:
        entries = resume.get(key, [])
        for index, item in enumerate(entries):
            _validate_resume_date(
                f"/{key}/{index}/date",
                item.get("date", None),
            )


def _validate_resume_metadata(resume: JsonResume) -> None:
    """Validate the metadata of a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        InvalidJsonResumeMetadataError: If the metadata of the JSON Resume is not valid.
    """
    if "meta" not in resume or "simpleResume" not in resume["meta"]:
        print_warning_message(
            "No metadata found in the resume. The metadata allows you to specify the template and "
            "language to be used when exporting or serving the resume. If these values are not "
            f"specified, the default language ({DEFAULT_LANGUAGE}) and template "
            f"({DEFAULT_TEMPLATE}) will be used. Alternatively, you can specify these values using "
            "command line arguments."
        )
        return

    metadata = resume["meta"]["simpleResume"]
    try:
        validate(
            instance=metadata,
            schema=json.load(Path.open(SIMPLE_RESUME_METADATA_SCHEMA_PATH, encoding="utf-8")),
        )
    except ValidationError as error:
        raise InvalidJsonResumeMetadataError() from error

    if (language := metadata.get("language")) is None:
        print_warning_message(
            "A language is not specified in the resume metadata, so unless specified by a command "
            f"line argument, the default language ({DEFAULT_LANGUAGE}) will be used when exporting "
            "or serving the resume."
        )
    elif language not in (supported_languages := get_supported_languages()):
        error_message = (
            f"The language '{language}' is not supported, the supported languages are: "
            f"{supported_languages}."
        )
        raise InvalidJsonResumeMetadataError(error_message)

    if (template := metadata.get("template")) is None:
        print_warning_message(
            "A template is not specified in the resume metadata, so unless specified by a command "
            f"line argument, the default template ({DEFAULT_TEMPLATE}) will be used when exporting "
            "or serving the resume."
        )
    elif template not in (registered_templates := get_registered_templates()):
        error_message = (
            f"The template '{template}' does not exist, the registered templates are: "
            f"{registered_templates}."
        )
        raise InvalidJsonResumeMetadataError(error_message)


def _validate_resume_version(resume: JsonResume) -> None:
    """Validate if the version of a JSON Resume is supported.

    Args:
        resume: The content of a JSON Resume file.

    Raises:
        UnsupportedJsonResumeVersionError: If the version of the JSON Resume is not supported.
    """
    if (schema_url := resume.get("$schema")) and schema_url != JSON_RESUME_SCHEMA_URL:
        raise UnsupportedJsonResumeVersionError(schema_url)
