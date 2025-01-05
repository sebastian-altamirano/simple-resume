"""Contains helpers to print messages."""

from __future__ import annotations

from rich import print


def print_error_message(message: str) -> None:
    """Print an error message.

    Args:
        message: The message to print.
    """
    _print_colored_message("red", message)


def print_info_message(message: str) -> None:
    """Print an info message.

    Args:
        message: The message to print.
    """
    _print_colored_message("blue", message)


def print_success_message(message: str) -> None:
    """Print a success message.

    Args:
        message: The message to print.
    """
    _print_colored_message("green", message)


def print_warning_message(message: str) -> None:
    """Print a warning message.

    Args:
        message: The message to print.
    """
    _print_colored_message("yellow", message)


def _print_colored_message(color: str, message: str) -> None:
    """Print a colored message.

    Args:
        color: The color of the message.
        message: The message to print.
    """
    print(f"[{color}]{message}[/{color}]\n")
