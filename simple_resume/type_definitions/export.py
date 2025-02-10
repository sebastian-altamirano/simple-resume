"""Contains type definitions related to the export process."""

from __future__ import annotations

from enum import Enum


class SupportedBrowserChannel(str, Enum):
    """Browser channels supported by Simple Resume."""

    GoogleChrome = "chrome"
    MicrosoftEdge = "msedge"
