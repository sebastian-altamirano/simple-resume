"""Contains type definitions related to JSON Resume."""

from __future__ import annotations

from typing import TypedDict


class JsonResumeBasics(TypedDict, total=False):
    """`/basics` field of the JSON Resume spec."""

    name: str
    label: str
    image: str
    email: str
    phone: str
    url: str
    summary: str
    location: JsonResumeBasicsLocation
    profiles: list[JsonResumeBasicsProfile]


class JsonResumeBasicsLocation(TypedDict, total=False):
    """`/basics/location` field of the JSON Resume spec."""

    address: str
    postalCode: str
    city: str
    countryCode: str
    region: str


class JsonResumeBasicsProfile(TypedDict, total=False):
    """`/basics/profiles/{index}` field of the JSON Resume spec."""

    network: str
    username: str
    url: str


class JsonResumeWork(TypedDict, total=False):
    """`/work/{index}` field of the JSON Resume spec."""

    name: str
    location: str
    description: str
    position: str
    url: str
    startDate: str
    endDate: str
    summary: str
    highlights: list[str]


class JsonResumeVolunteer(TypedDict, total=False):
    """`/volunteer/{index}` field of the JSON Resume spec."""

    organization: str
    position: str
    url: str
    startDate: str
    endDate: str
    summary: str
    highlights: list[str]


class JsonResumeEducation(TypedDict, total=False):
    """`/education/{index}` field of the JSON Resume spec."""

    institution: str
    url: str
    area: str
    studyType: str
    startDate: str
    endDate: str
    score: str
    courses: list[str]


class JsonResumeAward(TypedDict, total=False):
    """`/awards/{index}` field of the JSON Resume spec."""

    title: str
    date: str
    awarder: str
    summary: str


class JsonResumeCertificate(TypedDict, total=False):
    """`/certificates/{index}` field of the JSON Resume spec."""

    name: str
    date: str
    url: str
    issuer: str


class JsonResumePublication(TypedDict, total=False):
    """`/publications/{index}` field of the JSON Resume spec."""

    name: str
    publisher: str
    releaseDate: str
    url: str
    summary: str


class JsonResumeSkill(TypedDict, total=False):
    """`/skills/{index}` field of the JSON Resume spec."""

    name: str
    level: str
    keywords: list[str]


class JsonResumeLanguage(TypedDict, total=False):
    """`/languages/{index}` field of the JSON Resume spec."""

    language: str
    fluency: str


class JsonResumeInterest(TypedDict, total=False):
    """`/interests/{index}` field of the JSON Resume spec."""

    name: str
    keywords: list[str]


class JsonResumeReference(TypedDict, total=False):
    """`/references/{index}` field of the JSON Resume spec."""

    name: str
    reference: str


class JsonResumeProject(TypedDict, total=False):
    """`/projects/{index}` field of the JSON Resume spec."""

    name: str
    description: str
    highlights: list[str]
    keywords: list[str]
    startDate: str
    endDate: str
    url: str
    roles: list[str]
    entity: str
    type: str


class JsonResumeMeta(TypedDict, total=False):
    """`/meta` field of the JSON Resume spec."""

    canonical: str
    version: str
    lastModified: str
    simpleResume: SimpleResumeMetadata


class SimpleResumeMetadata(TypedDict, total=False):
    """Metadata supported by Simple Resume for a JSON Resume.

    It can be found in `/meta/simpleResume` of the JSON Resume.
    """

    language: str
    template: str


JsonResume = TypedDict(
    "JsonResume",
    {
        "$schema": str,
        "basics": JsonResumeBasics,
        "work": list[JsonResumeWork],
        "volunteer": list[JsonResumeVolunteer],
        "education": list[JsonResumeEducation],
        "awards": list[JsonResumeAward],
        "certificates": list[JsonResumeCertificate],
        "publications": list[JsonResumePublication],
        "skills": list[JsonResumeSkill],
        "languages": list[JsonResumeLanguage],
        "interests": list[JsonResumeInterest],
        "references": list[JsonResumeReference],
        "projects": list[JsonResumeProject],
        "meta": JsonResumeMeta,
    },
    total=False,
)
"""JSON Resume v1.0.0.

Check the [JSON Schema](https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json)
for the meaning of each field.
"""
