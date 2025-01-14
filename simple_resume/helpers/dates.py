"""Contains helpers to work with dates."""

from __future__ import annotations

from datetime import datetime


def parse_date(date: str) -> datetime:
    """Construct a `datetime` from an ISO 8601 date string.

    Args:
        date: The ISO 8601 date string to parse.

    Returns:
        The parsed date.

    Raises:
        ValueError: If the date string does not conform to ISO 8601.
    """
    return datetime.fromisoformat(date).astimezone()


def get_current_date() -> datetime:
    """Construct a `datetime` using the current date and time in the local timezone.

    Returns:
        The current date and time.
    """
    return datetime.now().astimezone()
