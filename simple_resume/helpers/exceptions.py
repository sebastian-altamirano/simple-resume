"""Contains exceptions."""

from __future__ import annotations

from simple_resume.helpers.constants import JSON_RESUME_SCHEMA_URL


class InvalidJsonResumeContentError(Exception):
    """Exception raised when the content of a JSON Resume is not valid."""

    def __init__(self) -> None:
        super().__init__("The content of the JSON Resume is not valid.")


class InvalidJsonResumeMetadataError(Exception):
    """Exception raised when the Simple Resume metadata of a JSON Resume is not valid.

    Args:
        additional_message: An additional message to append to the base message. It can be used to
            give a more detailed explanation of why the metadata is invalid.
    """

    def __init__(self, additional_message: str | None = None) -> None:
        base_message = (
            "The Simple Resume metadata (`/meta/simpleResume`) of the JSON Resume is not valid."
        )
        super().__init__(
            f"{base_message} {additional_message}" if additional_message else base_message
        )


class UnsupportedJsonResumeVersionError(Exception):
    """Exception raised when an unsupported version of a JSON Resume is used.

    The version of a JSON Resume is determined from the value of `/$schema`.

    Args:
        schema_url: The URL of the invalid JSON Schema (`/$schema` in the JSON Resume).
    """

    def __init__(self, schema_url: str) -> None:
        super().__init__(
            "Simple Resume only supports JSON Resume v1.0.0 from the original source "
            f"({JSON_RESUME_SCHEMA_URL}), but the resume is using a different version: "
            f"{schema_url}."
        )
