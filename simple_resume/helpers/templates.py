"""Contains helpers to work with Jinja templates."""

from __future__ import annotations

from simple_resume.helpers.constants import TEMPLATES_PATH


def get_registered_templates() -> list[str]:
    """Return the names of the registered templates."""
    return [path.name for path in TEMPLATES_PATH.glob("*") if path.is_dir()]
