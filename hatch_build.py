"""Hatchling build hook plugin."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from hatchling.builders.config import BuilderConfig
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface[BuilderConfig]):
    """Hook that performs specific tasks during the build process."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:  # noqa: ARG002
        """Prepare the environment for building."""
        if self.target_name == "wheel":
            subprocess.run(["poe", "compile-messages"], check=True)
            subprocess.run(["poe", "download-assets"], check=True)
            subprocess.run(["poe", "create-version-info-file", "hatchling"], check=True)

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:  # noqa: ARG002
        """Clean up after building."""
        if self.target_name == "wheel":
            (Path(__file__).parent / "simple_resume" / "VERSION_INFO").unlink(missing_ok=True)
