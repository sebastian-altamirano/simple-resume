"""Contains type definitions related to the export process."""

from __future__ import annotations

from enum import Enum


class SupportedPaperSize(str, Enum):
    """Paper sizes supported by Simple Resume."""

    A4 = "A4"
    Letter = "Letter"


class SupportedBrowserChannel(str, Enum):
    """Browser channels supported by Simple Resume."""

    GoogleChrome = "chrome"
    MicrosoftEdge = "msedge"
