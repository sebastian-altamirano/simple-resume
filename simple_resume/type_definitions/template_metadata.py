"""Contains type definitions related to the metadata of the templates."""

from __future__ import annotations

from enum import Enum
from typing import Literal


class ColorSystem(str, Enum):
    """Color systems supported by Simple Resume."""

    OpenColor = "Open Color"
    RadixColors = "Radix Colors"
    ReasonableColors = "Reasonable Colors"


ResumeSection = Literal[
    "About Me",
    "Awards",
    "Certificates",
    "Education",
    "Experience",
    "Interests",
    "Languages",
    "Projects",
    "Publications",
    "References",
    "Skills",
    "Volunteer",
]
