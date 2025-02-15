"""Hatchling build hook plugin."""

from __future__ import annotations

import subprocess
from typing import Any

from hatchling.builders.config import BuilderConfig
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface[BuilderConfig]):
    """Custom build hook to prepare the environment for building."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:  # noqa: ARG002
        """Download assets and compile messages before building."""
        if self.target_name == "wheel":
            subprocess.run(["poe", "compile-messages"], check=True)
            subprocess.run(["poe", "download-assets"], check=True)
