# Development

## Requirements

To work on this project you need to have the following installed:

- [Python](https://www.python.org/downloads/): The version specified in [`.python-version`](../.python-version) or a newer one.
- [uv](https://docs.astral.sh/uv/getting-started/installation/): Used as project and package manager.
- [Node.js](https://nodejs.org/en/download): Required for JavaScript-based development tools.
- Google Chrome or Microsoft Edge: Required by the `export` command to generate a PDF file. If no compatible browser is installed, you can include the `--install-browser` flag when running the `export` command to automatically install one.

## Setup

Once all requirements are met, you can set up the development environment:

```bash
# Clone the repository using your preferred cloning method.
git clone git@github.com:sebastian-altamirano/simple-resume.git
cd simple-resume
# Create the Python virtual environment and install the project dependencies.
uv sync
# Install the template dependencies (see `frontman.json`).
uv run poe download-assets
# Compile the translations.
uv run poe compile-messages
# Install JavaScript-based development tools.
npm install
```

Now you can run the local version of Simple Resume using `uv run simple-resume ...`, for example:

```bash
uv run simple-resume serve
uv run simple-resume export simple_resume/sample_data/resume.en.json
```

Alternatively, activate `.venv` and then invoke `simple-resume` directly.

### Development checks

You can format and lint the code with the following commands:

```bash
uv run poe format
uv run poe check
```

### Debugging

If you are using VSCode, it will pick up the configurations defined in the project's [`launch.json`](../.vscode/launch.json). These configurations allow you to debug all the commands supported by the application.

## Resume templates

The templates are written using [JinjaX](https://jinjax.scaletti.dev/), which is similar to Jinja but introduces the concept of components to improve clarity.

### Template dependencies

The templates may depend on external assets (fonts, stylesheets, icons, etc.), which can be installed with:

```bash
uv run poe download-assets
```

These assets are listed in the `frontman.json` file. This file is used by [frontman](https://github.com/livioribeiro/frontman) to download the dependencies to `simple-resume/static`.

For further instructions on adding new dependencies, consult the [frontman documentation](https://github.com/livioribeiro/frontman).

## Translations

Translations are managed using `.po` files located in `simple_resume/translations/<locale>/LC_MESSAGES/messages.po`.

`<locale>` represents the language for which the translation is provided (e.g. "es" for Spanish, "pt" for Portuguese, etc.).

The messages must be compiled before they can be used by the application. To compile them, run:

```bash
uv run poe compile-messages
```

Any untranslated messages will default to English.

### Adding translations for a new language

First, initialize the translation file by running:

```bash
uv run poe initialize-messages <locale>
```

This command creates `simple_resume/translations/<locale>/LC_MESSAGES/messages.po` pre-filled with empty translations. If you are unsure about the locale code, use:

```bash
uv run pybabel --list-locales
```

to see a list of available options.

### Adding or updating translations for a supported language

Simply run:

```bash
uv run poe update-messages
```

to extract and update the list of messages, then you can update the necessary translations in the `messages.po` files.

## Building

Use the appropriate command below to build the application for your desired target:

```bash
# Build the source distribution only.
uv build --sdist
# Build the wheel and run the custom Hatch wheel hook.
uv build --wheel
# Build both distributions.
uv build

# Can be used without Python on an OS compatible with the one used to produce the build.
uv run poe build-standalone
```

The source distribution and wheel can be published to PyPI and installed with `pipx` or `uvx`. The standalone build is a separate executable produced by PyInstaller.

Standalone builds are created with PyInstaller, which cannot cross-compile. This means you can only generate builds for your current operating system. Common workarounds include using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (to generate a Linux build from Windows) or [Docker](https://github.com/batonogov/docker-pyinstaller) (to generate a Linux build from Windows or a Windows build from Linux using Wine). [There are a few other catches that are documented in the PyInstaller documentation](https://pyinstaller.org/en/v6.12.0/usage.html#platform-specific-notes).
