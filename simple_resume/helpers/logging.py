"""Contains helpers to print messages."""

from __future__ import annotations

from rich import print


def print_info_message(message: str) -> None:
    """Print an info message.

    Args:
        message: The message to print.
    """
    print(f"[blue]{message}[/blue]")


def print_warning_message(message: str) -> None:
    """Print a warning message.

    Args:
        message: The message to print.
    """
    print(f"[yellow]{message}[/yellow]")
