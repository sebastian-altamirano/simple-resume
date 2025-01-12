"""Contains exceptions."""

from __future__ import annotations

from simple_resume.helpers.constants import JSON_RESUME_SCHEMA_URL


class EndDateBeforeStartDateError(Exception):
    """Exception raised when an end date is before a start date in a JSON Resume.

    Args:
        start_date_json_pointer: The JSON Pointer to the start date, e.g. `/work/0/startDate`.
        end_date_json_pointer: The JSON Pointer to the end date, e.g. `/work/0/endDate`.
        start_date: The start date.
        end_date: The end date.
    """

    def __init__(
        self,
        start_date_json_pointer: str,
        end_date_json_pointer: str,
        start_date: str,
        end_date: str,
    ) -> None:
        super().__init__(
            f"The end date '{end_date}' (`{end_date_json_pointer}`) cannot be earlier than the "
            f"start date '{start_date}' ({start_date_json_pointer})."
        )


class FutureDateError(Exception):
    """Exception raised when a date in a JSON Resume is in the future.

    Note: A future date is valid when used to indicate an expected date.

    Args:
        date_json_pointer: The JSON Pointer to the date, e.g. `/certificates/0/date`.
        date: The date that is in the future.
    """

    def __init__(
        self,
        date_json_pointer: str,
        date: str,
    ) -> None:
        super().__init__(f"The date '{date}' (`{date_json_pointer}`) cannot be in the future.")


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
