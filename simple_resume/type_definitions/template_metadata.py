"""Contains type definitions related to the metadata of the templates."""

from __future__ import annotations

from enum import Enum


class ColorSystem(str, Enum):
    """Color systems supported by Simple Resume."""

    OpenColor = "Open Color"
    RadixColors = "Radix Colors"
    ReasonableColors = "Reasonable Colors"
