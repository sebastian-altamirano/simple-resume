"""Contains helpers to work with Playwright."""

from __future__ import annotations

import subprocess

from playwright.sync_api import Browser, Error, Playwright

from simple_resume.helpers.cli_logging import print_error_message, print_info_message
from simple_resume.helpers.exceptions import BrowserNotFoundError
from simple_resume.type_definitions.export import SupportedBrowserChannel


def launch_browser(
    playwright: Playwright,
    browser_channel: SupportedBrowserChannel | None = None,
    *,
    should_install: bool = False,
) -> Browser:
    """Launch a browser, installing it if requested and necessary.

    Args:
        playwright: The Playwright instance to use.
        browser_channel: The browser channel to use. If `None`, it will try to use a browser
            installed in the system.
        should_install: Whether to install the specified browser if it is not already installed.

    Returns:
        The browser.

    Raises:
        BrowserNotFoundError: If no compatible browser is available.
        KeyboardInterrupt: If the browser installation is interrupted.
        subprocess.CalledProcessError: If the browser installation fails.
    """
    browser: Browser | None = None

    if browser_channel:
        print_info_message(f"Trying to use {get_browser_label(browser_channel)} as requested...")
        browser = _get_browser(playwright, browser_channel, should_install=should_install)
    elif not should_install:
        print_info_message("Trying to use a browser installed in the system...")
        supported_browser_channels = list(SupportedBrowserChannel)
        for channel in supported_browser_channels:
            if browser := _get_browser(playwright, channel, should_install=False):
                break
    else:
        # This should never happen because there is a validation in the CLI.
        raise ValueError("`should_install` cannot be `True` without specifying `browser_channel`.")

    if not browser:
        raise BrowserNotFoundError()

    return browser


def get_browser_label(browser_channel: SupportedBrowserChannel) -> str:
    """Get the label of a browser channel."""
    return {"chrome": "Google Chrome", "msedge": "Microsoft Edge"}[browser_channel]


def _get_browser(
    playwright: Playwright,
    browser_channel: SupportedBrowserChannel,
    *,
    should_install: bool = False,
) -> Browser | None:
    """Get a browser, installing it if requested and necessary.

    Args:
        playwright: The Playwright instance to use.
        browser_channel: The browser channel to use.
        should_install: Whether to install the browser if it is not already installed.

    Returns:
        The browser if it is installed, `None` otherwise.

    Raises:
        KeyboardInterrupt: If the browser installation is interrupted.
        subprocess.CalledProcessError: If the browser installation fails.
    """
    try:
        return playwright.chromium.launch(channel=browser_channel)
    except Error:
        if should_install:
            browser_label = get_browser_label(browser_channel)
            print_info_message(
                f"{browser_label} is not installed, will try to install it as requested..."
            )
            try:
                subprocess.run(
                    ["playwright", "install", browser_channel, "--with-deps"], check=True
                )
            except subprocess.CalledProcessError:
                print_error_message(f"{browser_label} installation failed.")
                raise
            except KeyboardInterrupt:
                print_error_message(f"{browser_label} installation was interrupted.")
                raise

            return playwright.chromium.launch(channel=browser_channel)
