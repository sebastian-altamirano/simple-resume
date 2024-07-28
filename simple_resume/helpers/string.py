"""Contains helpers to manipulate strings."""

from __future__ import annotations

import unicodedata


def remove_accents(value: str) -> str:
    """Remove accents from a string."""
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )
