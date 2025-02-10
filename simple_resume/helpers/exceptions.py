"""Contains custom exceptions."""

from __future__ import annotations


class BrowserNotFoundError(Exception):
    """Raised when a compatible browser is not found while exporting a resume."""

    def __init__(self) -> None:
        super().__init__(
            "No compatible browser found. Simple Resume requires a compatible browser to be "
            "installed to export the resume. Please rerun the command with `--browser` and "
            "`--install-browser` to install the specified browser before exporting the resume. "
            "Alternatively, you can install the browser manually."
        )
