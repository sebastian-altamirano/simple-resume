"""Contains Jinja filters."""

from __future__ import annotations

import re
from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Any

from babel import Locale

if TYPE_CHECKING:
    from collections.abc import Callable


def _add_colon_if_needed(value: str) -> str:
    """Add a colon at the end of a string if it does not already end with one.

    Args:
        value: The string to modify.

    Returns:
        The modified string.
    """
    return value if value.endswith(":") else f"{value}:"


def _change_date_format(iso_date: str, to_format: str) -> str:
    """Change the format of a date.

    Args:
        iso_date: Date in ISO format.
        to_format: Desired date format.

    Returns:
        The date in the desired format.
    """
    return datetime.fromisoformat(iso_date).strftime(to_format)


def _create_phone_number_url(phone_number: str) -> str:
    """Create a phone number URL.

    Args:
        phone_number: The phone number from which to create the URL.

    Returns:
        The phone number URL.
    """
    phone_number_without_separators = re.sub(r"[ ()]", "", phone_number)
    return f"tel:{phone_number_without_separators}"


def _get_country_name(language: str, country_code: str) -> str:
    """Get the localized country name.

    Args:
        country_code: An ISO 3166 country code.
        language: The language to use for localization.

    Returns:
        The localized country name.
    """
    return Locale(language).territories[country_code]


def get_all_custom_filters(language: str) -> dict[str, Callable[..., Any]]:
    """Return all custom filters provided by Simple Resume.

    Args:
        language: The language to use for localization.

    Returns:
        A dictionary containing the custom filters.
    """
    return {
        "addcolon": _add_colon_if_needed,
        "countryname": partial(_get_country_name, language),
        "dateformat": _change_date_format,
        "telurl": _create_phone_number_url,
    }
