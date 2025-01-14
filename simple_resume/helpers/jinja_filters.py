"""Contains Jinja filters."""

from __future__ import annotations

import re
from functools import partial
from typing import TYPE_CHECKING, Any, cast

from babel import Locale

from simple_resume.helpers.dates import get_current_date, parse_date

if TYPE_CHECKING:
    from collections.abc import Callable
    from gettext import NullTranslations


def _add_colon_if_needed(value: str) -> str:
    """Add a colon at the end of a string if it does not already end with one.

    Args:
        value: The string to modify.

    Returns:
        The modified string.
    """
    return value if value.endswith(":") else f"{value}:"


def _create_phone_number_url(phone_number: str) -> str:
    """Create a phone number URL.

    Args:
        phone_number: The phone number from which to create the URL.

    Returns:
        The phone number URL.
    """
    phone_number_without_separators = re.sub(r"[ ()]", "", phone_number)
    return f"tel:{phone_number_without_separators}"


def _format_date_for_resume(
    translations: NullTranslations, date_format: str, date: str | None
) -> str:
    """Format a date for a resume.

    Args:
        translations: The message catalog to use.
        date_format: The date format to use.
        date: The ISO 8601 date string to format, or `None` if not provided.

    Returns:
        The date in the specified format, or an empty string if no date was provided.
    """
    if not date:
        return ""

    parsed_date = parse_date(date)
    formatted_date = parsed_date.strftime(date_format)

    if parsed_date <= get_current_date():
        return formatted_date

    return f"{translations.gettext("Expected {date}").format(date=formatted_date)}"


def _format_date_range_for_resume(
    translations: NullTranslations, date_format: str, start_date: str | None, end_date: str | None
) -> str:
    """Format a date range for a resume.

    Note: It is assumed that both dates are valid, so no error handling is performed.

    Args:
        translations: The message catalog to use.
        date_format: The date format to use.
        start_date: The start date, or `None` if not provided.
        end_date: The end date, or `None` if not provided.

    Returns:
        The date range in the specified format, or an empty string if no dates were provided.
    """
    if not start_date and not end_date:
        return ""

    if not end_date:
        parsed_start_date = parse_date(cast(str, start_date))
        formatted_start_date = parsed_start_date.strftime(date_format)
        # `start_date` is assumed to be in the past.
        return f"{formatted_start_date} - {translations.gettext("Present")}"

    if not start_date:
        parsed_end_date = parse_date(end_date)
        formatted_end_date = parsed_end_date.strftime(date_format)
        if parsed_end_date <= get_current_date():
            return formatted_end_date

        return f"{translations.gettext("Expected {date}").format(date=formatted_end_date)}"

    parsed_start_date = parse_date(start_date)
    formatted_start_date = parsed_start_date.strftime(date_format)
    parsed_end_date = parse_date(end_date)
    formatted_end_date = parsed_end_date.strftime(date_format)
    # `start_date` is assumed to be earlier than or equal to `end_date`.
    if parsed_end_date <= get_current_date():
        return f"{formatted_start_date} - {formatted_end_date}"

    return (
        f"{formatted_start_date} - "
        f"{translations.gettext("Expected {date}").format(date=formatted_end_date)}"
    )


def _get_country_name(language: str, country_code: str) -> str:
    """Get the localized country name.

    Args:
        country_code: An ISO 3166 country code.
        language: The language to use for localization.

    Returns:
        The localized country name.
    """
    return Locale(language).territories[country_code]


def get_all_custom_filters(
    language: str, translations: NullTranslations
) -> dict[str, Callable[..., Any]]:
    """Return all custom filters provided by Simple Resume.

    Args:
        language: The language to use for localization.
        translations: The message catalog to use.

    Returns:
        A dictionary containing the custom filters.
    """
    return {
        "addcolon": _add_colon_if_needed,
        "countryname": partial(_get_country_name, language),
        "dateformat": partial(_format_date_for_resume, translations),
        "daterangeformat": partial(_format_date_range_for_resume, translations),
        "telurl": _create_phone_number_url,
    }
