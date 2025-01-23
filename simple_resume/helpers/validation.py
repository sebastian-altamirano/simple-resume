"""Contains helpers to validate JSON Resume files."""

from __future__ import annotations

import re
from string import Template
from typing import TYPE_CHECKING

import requests
from pydantic_core import PydanticCustomError

from simple_resume.helpers.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_TEMPLATE,
    LATEST_SUPPORTED_JSON_RESUME_SCHEMA_TAG,
)
from simple_resume.helpers.i18n import get_supported_languages
from simple_resume.helpers.logging import (
    print_warning_message,
)
from simple_resume.helpers.templates import get_registered_templates

if TYPE_CHECKING:
    from datetime import datetime

    from pydantic import HttpUrl
    from pydantic_extra_types.language_code import LanguageAlpha2


def validate_date_range(start_date: datetime | None, end_date: datetime | None) -> None:
    """Validate that the start date is before the end date.

    Raises:
        PydanticCustomError: If the end date is before the start date.
    """
    if not start_date or not end_date:
        return

    if end_date < start_date:
        raise PydanticCustomError(
            "end_date_before_start_date",  # noqa: EM101 Does not apply here.
            "The end date '{end_date}' cannot be earlier than the start date '{start_date}'.",
            {
                "end_date": end_date,
                "start_date": start_date,
            },
        )

    return


def validate_json_schema(json_schema: HttpUrl | None) -> None:
    """Validate if a JSON Schema is supported by Simple Resume.

    It does not raise an error if the JSON Schema is not compatible, but it prints a warning
    message. This is because, although Simple Resume is designed to work with the JSON Resume V1.Y.Z
    schema, it may still work without issues if the validation process is successful.

    Args:
        json_schema: The JSON Schema of a JSON Resume.
    """
    if not json_schema:
        print_warning_message(
            "The resume does not specify a JSON Schema. The validation process is still ongoing, "
            "but Simple Resume is designed to work with JSON Resume schema V1.Y.Z. To avoid this "
            f'warning, add `"$schema": "{_get_latest_supported_schema()}"` to your resume.'
        )
    elif not re.search(
        r"https:\/\/raw\.githubusercontent\.com\/jsonresume\/resume-schema\/v1\.\d+\.\d+\/schema\.json",
        str(json_schema),
    ):
        print_warning_message(
            "The resume specifies a JSON Schema different from the one Simple Resume supports or "
            "uses a different source than the original. The validation process is still ongoing, "
            "but Simple Resume is designed to work with JSON Resume schema V1.Y.Z. To avoid "
            "potential problems, change the schema to"
            f'`"$schema": "{_get_latest_supported_schema()}"` in your resume.'
        )


def validate_metadata_language(language: LanguageAlpha2 | None) -> None:
    """Validate the language specified in the Simple Resume metadata of a JSON Resume.

    Args:
        language: The language specified in the metadata.

    Raises:
        PydanticCustomError: If the language is not supported.
    """
    if language is None:
        print_warning_message(
            "A language is not specified in the resume metadata, so unless specified by a command "
            f"line argument, the default language ({DEFAULT_LANGUAGE}) will be used when exporting "
            "or serving the resume."
        )
    elif language not in (supported_languages := get_supported_languages()):
        raise PydanticCustomError(
            "metadata_language",  # noqa: EM101 Does not apply here.
            "The language '{language}' is not supported, the supported languages are: "
            "{supported_languages}.",
            {
                "language": language,
                "supported_languages": supported_languages,
            },
        )


def validate_metadata_template(template: str | None) -> None:
    """Validate the template specified in the Simple Resume metadata of a JSON Resume.

    Args:
        template: The template specified in the metadata.

    Raises:
        PydanticCustomError: If the template does not exist.
    """
    if template is None:
        print_warning_message(
            "A template is not specified in the resume metadata, so unless specified by a command "
            f"line argument, the default template ({DEFAULT_TEMPLATE}) will be used when exporting "
            "or serving the resume."
        )
    elif template not in (registered_templates := get_registered_templates()):
        raise PydanticCustomError(
            "metadata_template",  # noqa: EM101 Does not apply here.
            "The template '{template}' does not exist, the registered templates are: "
            "{registered_templates}.",
            {
                "template": template,
                "registered_templates": registered_templates,
            },
        )


def _get_latest_supported_schema() -> str:
    """Return the latest supported JSON Resume schema."""
    schema_template = Template(
        "https://raw.githubusercontent.com/jsonresume/resume-schema/$latest_supported_tag/schema.json"
    )
    latest_supported_tag: str = LATEST_SUPPORTED_JSON_RESUME_SCHEMA_TAG

    try:
        response = requests.get("https://api.github.com/repos/jsonresume/resume-schema/tags")
        response.raise_for_status()
        tags = response.json()
        # Tags are sorted by descending date.
        for tag in tags:
            if re.match(r"v1\.\d+\.\d+", tag["name"]):
                latest_supported_tag = tag["name"]
                break
    except requests.HTTPError:
        pass

    return schema_template.substitute(latest_supported_tag=latest_supported_tag)
