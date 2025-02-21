from __future__ import annotations

import platform
import shutil
import sys
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

import livereload
import pyinstaller_versionfile
from PyInstaller.utils.hooks import collect_submodules
from simple_resume.helpers.constants import PACKAGE_PATH, VERSION_INFO_PATH
from simple_resume.helpers.i18n import get_supported_languages

if TYPE_CHECKING:
    from PyInstaller.building.api import COLLECT, EXE, PYZ
    from PyInstaller.building.build_main import Analysis

# `PACKAGE_PATH` is used because `__file__` is not available in this context.
PROJECT_PATH = PACKAGE_PATH.parent
DIST_PATH = PROJECT_PATH / "dist"

project_metadata = tomllib.loads((PROJECT_PATH / "pyproject.toml").read_text(encoding="utf-8"))[
    "project"
]


def _cleanup() -> None:
    VERSION_INFO_PATH.unlink(missing_ok=True)


def _copy_license_and_readme(destination_path: str) -> None:
    license_path = PROJECT_PATH / "LICENSE.txt"
    readme_path = PROJECT_PATH / "README.md"

    shutil.copy(license_path, destination_path)
    shutil.copy(readme_path, destination_path)


def _create_windows_version_info_file() -> Path:
    author = project_metadata["authors"][0]["name"]

    output_file = DIST_PATH / "windows_version_info.txt"
    pyinstaller_versionfile.create_versionfile(
        company_name=author,
        file_description=project_metadata["description"],
        internal_name=project_metadata["name"],
        legal_copyright=f"Copyright (c) {author}",
        original_filename=f"{project_metadata['name']}.exe",
        output_file=output_file,
        product_name="Simple Resume",
        translations=[1033, 1200],
        version=project_metadata["version"],
    )
    return output_file


def _get_directory_paths() -> list[tuple[Path, Path]]:
    directories = [
        "components",
        "sample_data",
        "static",
        "templates",
    ]
    return [
        (full_path := Path("simple_resume") / directory, full_path) for directory in directories
    ]


def _get_translations_paths() -> list[tuple[Path, Path]]:
    supported_languages = get_supported_languages()

    paths: list[tuple[Path, Path]] = []
    for language in supported_languages:
        messages_path = Path("simple_resume") / "translations" / language / "LC_MESSAGES"
        paths.append((messages_path / "messages.mo", messages_path))

    return paths


def _make_archive() -> None:
    version = project_metadata["version"]
    system = platform.system().lower()
    system = "macos" if system == "darwin" else system
    architecture = platform.machine()
    architecture = "x86_64" if architecture in ("AMD64", "x86_64") else architecture

    shutil.make_archive(
        str(DIST_PATH / f"simple_resume-{version}-{system}-{architecture}"),
        "zip" if system == "windows" else "gztar",
        root_dir=DIST_PATH / "simple_resume",
        base_dir=".",
    )


if sys.platform == "win32":
    binaries = [(Path(".venv") / "Scripts" / "playwright.exe", "playwright")]
    windows_version_info_path = _create_windows_version_info_file()
else:
    binaries = [(Path(".venv") / "bin" / "playwright", "playwright")]
    windows_version_info_path = None


a = Analysis(
    [Path("simple_resume") / "__main__.py"],
    pathex=[],
    binaries=binaries,
    datas=[
        *_get_directory_paths(),
        *_get_translations_paths(),
        (Path("simple_resume") / "VERSION_INFO", "simple_resume"),
        (
            Path(livereload.__file__).parent / "vendors" / "livereload.js",
            Path("livereload") / "vendors",
        ),
    ],
    hiddenimports=[*collect_submodules("shellingham")],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [("O", None, "OPTION"), ("O", None, "OPTION")],
    exclude_binaries=True,
    name="simple-resume",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=windows_version_info_path,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="simple_resume",
)

_copy_license_and_readme(coll.name)
_make_archive()

_cleanup()
