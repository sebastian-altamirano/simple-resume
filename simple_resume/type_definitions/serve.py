"""Contains type definitions related to the serve process."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from multiprocessing import Process


class SimpleResumeServer(TypedDict):
    """Server process and other related information."""

    process: Process
    url: str
