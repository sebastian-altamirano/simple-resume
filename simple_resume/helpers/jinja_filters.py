"""Contains Jinja filters."""

from __future__ import annotations

import re
from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Any, cast, overload

from babel import Locale
from babel.lists import format_list
from pydantic import HttpUrl
from tldextract import tldextract

from simple_resume.helpers.dates import get_current_date
from simple_resume.helpers.networks import get_supported_networks
from simple_resume.models.json_resume import JsonResume, JsonResumeInterest, JsonResumeLanguage
from simple_resume.type_definitions.networks import NetworkInfo
from simple_resume.type_definitions.template_metadata import ResumeSection

if TYPE_CHECKING:
    from collections.abc import Callable

    from babel.support import NullTranslations


def get_all_custom_filters(
    language: str, translations: NullTranslations
) -> dict[str, Callable[..., Any]]:
    """Return all custom filters provided by Simple Resume.

    Args:
        language: The language to use for localization.
        translations: The message catalog to use.

    Returns:
        A dictionary containing the custom filters.
    """
    return {
        "addlocalizedcolon": partial(_add_localized_colon, translations),
        "countryname": partial(_get_country_name, language),
        "dateformat": partial(_format_date_for_resume, translations),
        "daterangeformat": partial(_format_date_range_for_resume, translations),
        "domainname": _get_domain_name,
        "mapinterests": partial(_map_interests, language),
        "maplanguages": _map_languages,
        "mapsections": _map_sections,
        "networkinfo": _get_network_info,
    }


def _add_localized_colon(translations: NullTranslations, label: str) -> str:
    """Add a localized colon at the end of a string, replacing the original colon if present.

    This is necessary because, for example, in French there is a space before the colon.

    Args:
        translations: The message catalog to use.
        label: The string to modify.

    Returns:
        The modified string with a localized colon.
    """
    return f"{translations.gettext('{label}:').format(label=label.removesuffix(':'))}"


def _format_date_for_resume(
    translations: NullTranslations, date_format: str, date: datetime | None
) -> str:
    """Format a date for a resume.

    Args:
        translations: The message catalog to use.
        date_format: The date format to use.
        date: The date to format, or `None` if not provided.

    Returns:
        The date in the specified format, or an empty string if no date was provided.
    """
    if not date:
        return ""

    formatted_date = date.strftime(date_format)

    if date <= get_current_date():
        return formatted_date

    return f"{translations.gettext('Expected {date}').format(date=formatted_date)}"


def _format_date_range_for_resume(
    translations: NullTranslations,
    date_format: str,
    start_date: datetime | None,
    end_date: datetime | None,
) -> str:
    """Format a date range for a resume.

    Args:
        translations: The message catalog to use.
        date_format: The date format to use.
        start_date: The start date, or `None` if not provided.
        end_date: The end date, or `None` if not provided.

    Returns:
        The date range in the specified format, or an empty string if no dates were provided.
    """
    if not start_date and not end_date:
        return ""

    if not end_date:
        start_date = cast(datetime, start_date)
        formatted_start_date = start_date.strftime(date_format)

        return (
            f"{formatted_start_date} - {translations.gettext('Present')}"
            if start_date <= get_current_date()
            else f"{translations.gettext('Expected {date}').format(date=formatted_start_date)}"
        )

    if not start_date:
        formatted_end_date = end_date.strftime(date_format)

        return (
            formatted_end_date
            if end_date <= get_current_date()
            else f"{translations.gettext('Expected {date}').format(date=formatted_end_date)}"
        )

    formatted_start_date = start_date.strftime(date_format)
    formatted_end_date = end_date.strftime(date_format)

    # The filter assumes that its inputs are validated, so it expects `start_date` to be earlier
    # than or equal to `end_date`.
    return (
        f"{formatted_start_date} - {formatted_end_date}"
        if end_date <= get_current_date()
        else (
            f"{formatted_start_date} - "
            f"{translations.gettext('Expected {date}').format(date=formatted_end_date)}"
        )
    )


def _get_country_name(language: str, country_code: str) -> str:
    """Get the localized country name.

    Args:
        language: The language to use for localization.
        country_code: An ISO 3166 country code.

    Returns:
        The localized country name.
    """
    return Locale(language).territories[country_code]


@overload
def _get_domain_name(url: HttpUrl) -> str: ...
@overload
def _get_domain_name(url: None) -> None: ...
def _get_domain_name(url: HttpUrl | None) -> str | None:
    """Extract the domain name from a URL.

    Args:
        url: The URL, or `None` if not provided.

    Returns:
        The domain name, or `None` if the URL is not provided.
    """
    return tldextract.extract(str(url)).domain if url else None


def _get_network_info(network: str | None, url: HttpUrl | None) -> NetworkInfo | None:
    """Get the network information for a supported network.

    Args:
        network: The network name, or `None` if not provided.
        url: The network URL, or `None` if not provided.

    Returns:
        The network information if the network is supported, or `None` if it is not supported or
        could not be determined.
    """
    supported_networks = get_supported_networks()

    if network:
        normalized_network = re.sub(r"\s+", "", network.lower())
        if network_info := supported_networks.get(normalized_network):
            return network_info
    if url:
        extracted_url = tldextract.extract(str(url))

        return (
            # From most specific to least specific.
            supported_networks.get(extracted_url.fqdn)
            or supported_networks.get(f"{extracted_url.subdomain}.{extracted_url.domain}")
            or supported_networks.get(extracted_url.domain)
        )

    return None


def _map_interests(language: str, interests: list[JsonResumeInterest]) -> list[str]:
    """Map the interests to a list of strings.

    Args:
        language: The language to use for localization.
        interests: The interests to map.

    Returns:
        The mapped interests.
    """
    return [
        f"{interest.name} ({format_list(interest.keywords, locale=language)})"
        if interest.keywords
        else interest.name
        for interest in interests
        if interest.name
    ]


def _map_languages(languages: list[JsonResumeLanguage]) -> list[str]:
    """Map the languages to a list of strings."""
    return [
        f"{language.language} ({language.fluency})" if language.fluency else language.language
        for language in languages
        if language.language
    ]


def _map_sections(
    sections: list[ResumeSection],
    resume: JsonResume,
    unsupported_sections: list[ResumeSection] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Map the resume sections to components.

    Args:
        sections: The resume sections, arranged in order of display.
        resume: A validated JSON Resume.
        unsupported_sections: The resume sections that are not supported by the template.

    Returns:
        A list of tuples containing the component name and its props.
    """
    components: dict[ResumeSection, tuple[str, dict[str, Any]]] = {
        "About Me": ("About", {"summary": resume.basics.summary}),
        "Awards": ("Awards", {"awards": resume.awards}),
        "Certificates": ("Certificates", {"certificates": resume.certificates}),
        "Education": ("EducationHistory", {"education_history": resume.education}),
        "Experience": ("WorkExperience", {"work_experience": resume.work}),
        "Interests": ("Interests", {"interests": resume.interests}),
        "Languages": ("Languages", {"languages": resume.languages}),
        "Projects": ("Projects", {"projects": resume.projects}),
        "Publications": ("Publications", {"publications": resume.publications}),
        "References": (
            "References",
            {
                "references": resume.references,
                "references_on_request": resume.meta.simple_resume.template.references_on_request,
            },
        ),
        "Skills": (
            "Skills",
            {"interests": resume.interests, "languages": resume.languages, "skills": resume.skills},
        ),
        "Volunteer": ("Volunteer", {"volunteer": resume.volunteer}),
    }

    unsupported_sections_set = set(unsupported_sections or [])
    return [components[section] for section in sections if section not in unsupported_sections_set]
