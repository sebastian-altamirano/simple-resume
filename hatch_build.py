"""Hatchling build hook plugin."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from hatchling.builders.config import BuilderConfig
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface[BuilderConfig]):
    """Hook that performs specific tasks during the build process."""

    def _run_poe_task(self, *args: str) -> None:
        """Run a Poe task directly in Hatch's isolated build environment.

        Poe's automatic executor detects uv projects and delegates tasks to `uv run`. During
        `uv sync`, uv already holds the project lock while invoking this hook, so delegating back to
        uv would deadlock waiting for that same lock.
        """
        subprocess.run(["poe", "--executor", "simple", *args], check=True)

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:  # noqa: ARG002
        """Prepare the environment for building."""
        if self.target_name == "wheel":
            self._run_poe_task("compile-messages")
            self._run_poe_task("download-assets")
            self._run_poe_task("create-version-info-file", "hatchling")

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:  # noqa: ARG002
        """Clean up after building."""
        if self.target_name == "wheel":
            (Path(__file__).parent / "simple_resume" / "VERSION_INFO").unlink(missing_ok=True)
