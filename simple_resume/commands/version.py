"""Contains the logic of the `version` command."""

from __future__ import annotations

import pickle
import platform
import sys

import rich
from rich.panel import Panel

from simple_resume.helpers.constants import VERSION_INFO_PATH


def _create_panel(title: str, key_value_pairs: dict[str, str]) -> Panel:
    return Panel(
        "\n".join(f"[blue]{key}:[/blue]\n{value}" for key, value in key_value_pairs.items()),
        title=f"[blue]{title}[/blue]",
    )


def version() -> None:
    """Display the version information."""
    panels: list[Panel] = []

    if VERSION_INFO_PATH.exists():
        version_info = pickle.loads(VERSION_INFO_PATH.read_bytes())
        build_info = {
            "Simple Resume version": version_info["app_version"],
            "Git commit hash": version_info["git_commit_hash"],
            "OS platform": version_info["os_platform"],
            "Build system": version_info["build_system"],
            "Python version": version_info["python_version"],
            "Date": version_info["build_date"],
        }
        panels.append(_create_panel("Build Information", build_info))
    else:
        build_info = {"Simple Resume version": "Development"}
        panels.append(_create_panel("Build Information", build_info))

    runtime_info = {
        "OS platform": platform.platform(),
        "Python version": sys.version,
        "Python executable": sys.executable,
    }
    panels.append(_create_panel("Runtime Information", runtime_info))

    rich.print(*panels)
