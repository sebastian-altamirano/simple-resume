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

PACKAGE_PATH = Path(__file__).parent.parent

COMPONENTS_PATH = PACKAGE_PATH / "components"
SAMPLE_DATA_PATH = PACKAGE_PATH / "sample_data"
STATIC_PATH = PACKAGE_PATH / "static"
TEMPLATES_PATH = PACKAGE_PATH / "templates"
TRANSLATIONS_PATH = PACKAGE_PATH / "translations"

SAMPLE_RESUME_PATH = SAMPLE_DATA_PATH / "resume.en.json"
