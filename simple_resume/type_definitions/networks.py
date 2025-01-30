"""Contains type definitions related to networks."""

from __future__ import annotations

from typing import TypedDict


class NetworkIconIds(TypedDict):
    """The icon ID of a network for all the supported sprite sheets."""

    bootstrap: str | None


class NetworkInfo(TypedDict):
    """Information about a network, e.g. LinkedIn, GitHub, X, etc."""

    icon_id: NetworkIconIds
    """The icon ID of the network for all the supported sprite sheets."""
    label: str
    """The name of the network."""
