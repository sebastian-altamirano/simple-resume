"""Contains helpers to work with dates."""

from __future__ import annotations

from datetime import datetime


def get_current_date() -> datetime:
    """Construct a `datetime` using the current date and time in the local timezone.

    Returns:
        The current date and time.
    """
    return datetime.now().astimezone()


def to_aware_datetime(date: datetime) -> datetime:
    """Convert a `datetime` to an aware `datetime`.

    Args:
        date: The `datetime` to convert.

    Returns:
        The `datetime` as an aware `datetime`.
    """
    return date.astimezone(date.tzinfo)
