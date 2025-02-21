"""Contains build helpers."""

from __future__ import annotations

import importlib.metadata
import os
import pickle
import platform
import subprocess
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from simple_resume.helpers.constants import VERSION_INFO_PATH


def create_version_info_file(build_system: Literal["hatchling", "pyinstaller"]) -> None:
    """Create a file with build information."""
    valid_build_systems = ["hatchling", "pyinstaller"]
    if build_system not in valid_build_systems:
        raise ValueError(
            f"Invalid build system: {build_system}. Must be one of {valid_build_systems}."
        )

    try:
        app_version = importlib.metadata.version("simple_resume")
    except importlib.metadata.PackageNotFoundError:
        app_version = tomllib.loads(
            (Path(__file__).parent.parent / "pyproject.toml").read_text(encoding="utf-8")
        )["project"]["version"]

    try:
        git_commit_hash = (
            os.environ.get("GIT_COMMIT_HASH", None)
            or subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, check=True, text=True
            ).stdout.strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_commit_hash = "Unknown"

    version_info = {
        "app_version": app_version,
        "build_date": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "build_system": (
            f"{'Hatchling' if build_system == 'hatchling' else 'PyInstaller'} "
            f"{importlib.metadata.version(build_system)}"
        ),
        "git_commit_hash": git_commit_hash,
        "os_platform": platform.platform(),
        "python_version": sys.version,
    }

    # Write the version information to a binary file to prevent accidental modifications.
    VERSION_INFO_PATH.write_bytes(pickle.dumps(version_info))
