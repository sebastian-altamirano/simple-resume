"""Contains helpers to print messages."""

from __future__ import annotations

from rich import print


def print_error_message(message: str) -> None:
    """Print an error message.

    Args:
        message: The message to print.
    """
    print(f"[red]{message}[/red]")


def print_info_message(message: str) -> None:
    """Print an info message.

    Args:
        message: The message to print.
    """
    print(f"[blue]{message}[/blue]")


def print_success_message(message: str) -> None:
    """Print a success message.

    Args:
        message: The message to print.
    """
    print(f"[green]{message}[/green]")
