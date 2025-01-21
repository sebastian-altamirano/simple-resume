"""Contains constants."""

from __future__ import annotations

from pathlib import Path

DEFAULT_LANGUAGE = "en"
DEFAULT_OUTPUT_PATH = Path("~/Desktop").expanduser()
DEFAULT_PORT = 5000
DEFAULT_TEMPLATE = "basic"

LATEST_SUPPORTED_JSON_RESUME_SCHEMA_TAG = "v1.2.1"
"""The latest supported JSON Resume schema tag that was tested, but any V1.Y.Z resume should work
with the tool."""

PACKAGE_PATH = (Path(__file__) / ".." / "..").resolve()

COMPONENTS_PATH = (PACKAGE_PATH / "components").resolve()
SAMPLE_DATA_PATH = (PACKAGE_PATH / "sample_data").resolve()
STATIC_PATH = (PACKAGE_PATH / "static").resolve()
TEMPLATES_PATH = (PACKAGE_PATH / "templates").resolve()
TRANSLATIONS_PATH = (PACKAGE_PATH / "translations").resolve()

SAMPLE_RESUME_PATH = (SAMPLE_DATA_PATH / "resume.en.json").resolve()
