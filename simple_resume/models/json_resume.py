"""Contains models related to the JSON Resume schema."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    PastDatetime,
)
from pydantic.alias_generators import to_camel
from pydantic.functional_validators import AfterValidator, field_validator, model_validator
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.language_code import LanguageAlpha2
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_extra_types.semantic_version import SemanticVersion

from simple_resume.helpers.dates import to_aware_datetime
from simple_resume.helpers.validation import (
    validate_color_scheme,
    validate_date_range,
    validate_json_schema_url,
    validate_metadata_language,
    validate_metadata_template,
)
from simple_resume.type_definitions.template_metadata import ColorSystem

_DateTime = Annotated[
    datetime,
    AfterValidator(to_aware_datetime),
]

_PastDateTime = Annotated[
    PastDatetime,
    AfterValidator(to_aware_datetime),
]


class JsonResumeBaseModel(BaseModel):
    """Base model with common configuration for models related to the JSON Resume schema."""

    model_config = ConfigDict(
        alias_generator=to_camel, extra="allow", frozen=True, str_strip_whitespace=True
    )


class JsonResumeBasicsLocation(JsonResumeBaseModel):
    """`/basics/location` field of the JSON Resume spec."""

    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country_code: CountryAlpha2 | None = None
    region: str | None = None


class JsonResumeBasics(JsonResumeBaseModel):
    """`/basics` field of the JSON Resume spec."""

    name: str | None = None
    label: str | None = None
    image: HttpUrl | None = None
    email: EmailStr | None = None
    phone: PhoneNumber | None = None
    url: HttpUrl | None = None
    summary: str | None = None
    location: JsonResumeBasicsLocation = Field(default_factory=JsonResumeBasicsLocation)
    profiles: list[JsonResumeBasicsProfile] = Field(default_factory=list)


class JsonResumeBasicsProfile(JsonResumeBaseModel):
    """`/basics/profiles/{index}` field of the JSON Resume spec."""

    network: str | None = None
    username: str | None = None
    url: HttpUrl | None = None


class JsonResumeWork(JsonResumeBaseModel):
    """`/work/{index}` field of the JSON Resume spec."""

    name: str | None = None
    location: str | None = None
    description: str | None = None
    position: str | None = None
    url: HttpUrl | None = None
    start_date: _DateTime | None = None
    end_date: _DateTime | None = None
    summary: str | None = None
    highlights: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_start_date_is_before_end_date(self) -> Self:
        """Validate that the start date is before the end date.

        Raises:
            PydanticCustomError: If the end date is before the start date.
        """
        validate_date_range(self.start_date, self.end_date)
        return self


class JsonResumeVolunteer(JsonResumeBaseModel):
    """`/volunteer/{index}` field of the JSON Resume spec."""

    organization: str | None = None
    position: str | None = None
    url: HttpUrl | None = None
    start_date: _DateTime | None = None
    end_date: _DateTime | None = None
    summary: str | None = None
    highlights: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_start_date_is_before_end_date(self) -> Self:
        """Validate that the start date is before the end date.

        Raises:
            PydanticCustomError: If the end date is before the start date.
        """
        validate_date_range(self.start_date, self.end_date)
        return self


class JsonResumeEducation(JsonResumeBaseModel):
    """`/education/{index}` field of the JSON Resume spec."""

    institution: str | None = None
    url: HttpUrl | None = None
    area: str | None = None
    study_type: str | None = None
    start_date: _DateTime | None = None
    end_date: _DateTime | None = None
    score: str | None = None
    courses: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_start_date_is_before_end_date(self) -> Self:
        """Validate that the start date is before the end date.

        Raises:
            PydanticCustomError: If the end date is before the start date.
        """
        validate_date_range(self.start_date, self.end_date)
        return self


class JsonResumeAward(JsonResumeBaseModel):
    """`/awards/{index}` field of the JSON Resume spec."""

    title: str | None = None
    date: _DateTime | None = None
    awarder: str | None = None
    summary: str | None = None


class JsonResumeCertificate(JsonResumeBaseModel):
    """`/certificates/{index}` field of the JSON Resume spec."""

    name: str | None = None
    date: _DateTime | None = None
    url: HttpUrl | None = None
    issuer: str | None = None


class JsonResumePublication(JsonResumeBaseModel):
    """`/publications/{index}` field of the JSON Resume spec."""

    name: str | None = None
    publisher: str | None = None
    release_date: _DateTime | None = None
    url: HttpUrl | None = None
    summary: str | None = None


class JsonResumeSkill(JsonResumeBaseModel):
    """`/skills/{index}` field of the JSON Resume spec."""

    name: str | None = None
    level: str | None = None
    keywords: list[str] = Field(default_factory=list)


class JsonResumeLanguage(JsonResumeBaseModel):
    """`/languages/{index}` field of the JSON Resume spec."""

    language: str | None = None
    fluency: str | None = None


class JsonResumeInterest(JsonResumeBaseModel):
    """`/interests/{index}` field of the JSON Resume spec."""

    name: str | None = None
    keywords: list[str] = Field(default_factory=list)


class JsonResumeReference(JsonResumeBaseModel):
    """`/references/{index}` field of the JSON Resume spec."""

    name: str | None = None
    reference: str | None = None


class JsonResumeProject(JsonResumeBaseModel):
    """`/projects/{index}` field of the JSON Resume spec."""

    name: str | None = None
    description: str | None = None
    highlights: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    start_date: _DateTime | None = None
    end_date: _DateTime | None = None
    url: HttpUrl | None = None
    roles: list[str] = Field(default_factory=list)
    entity: str | None = None
    type: str | None = None

    @model_validator(mode="after")
    def check_start_date_is_before_end_date(self) -> Self:
        """Validate that the start date is before the end date.

        Raises:
            PydanticCustomError: If the end date is before the start date.
        """
        validate_date_range(self.start_date, self.end_date)
        return self


class SimpleResumeTemplateMetadata(JsonResumeBaseModel):
    """Extended template metadata."""

    color_scheme: dict[str, str] | None = None
    color_system: ColorSystem | None = None
    name: Annotated[str, AfterValidator(validate_metadata_template)]

    @model_validator(mode="after")
    def check_color_scheme_respects_color_system(self) -> Self:
        """Validate that the color scheme respects the color system.

        Raises:
            PydanticCustomError: If the color system is not specified or if the color scheme does
                not match the color system.
        """
        validate_color_scheme(self.color_system, self.color_scheme)
        return self


class SimpleResumeMetadata(JsonResumeBaseModel):
    """Metadata supported by Simple Resume for a JSON Resume.

    It can be found in `/meta/simpleResume` of the JSON Resume.
    """

    language: Annotated[LanguageAlpha2 | None, AfterValidator(validate_metadata_language)] = Field(
        default=None,
        validate_default=True,
    )
    template: (
        Annotated[str | None, AfterValidator(validate_metadata_template)]
        | SimpleResumeTemplateMetadata
    ) = Field(
        default=None,
        validate_default=True,
    )


class JsonResumeMeta(JsonResumeBaseModel):
    """`/meta` field of the JSON Resume spec."""

    canonical: HttpUrl | None = None
    version: SemanticVersion | None = None
    last_modified: _PastDateTime | None = None
    simple_resume: SimpleResumeMetadata = Field(default_factory=SimpleResumeMetadata)

    @field_validator("version", mode="before")
    @classmethod
    def fix_resume_version(cls, version: str) -> str | None:
        """Fix the version used in `/meta/version` of a JSON Resume.

        The description of `/meta/version` in the JSON Resume schema is: "A version field which
        follows semver - e.g. v1.0.0", but according to https://semver.org/#is-v123-a-semantic-version,
        "v1.0.0" is not a semantic version, "1.0.0" is, so this function removes the "v" from the
        version.
        """
        try:
            if version[0] == "v":
                return version[1:]
        except IndexError:
            pass

        return version


class JsonResume(JsonResumeBaseModel):
    """JSON Resume v1.Y.Z.

    Check the [JSON Schema](https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json)
    for the meaning of each field.

    This implementation is similar to the schema, but it has some differences in terms of validation
    that may break compatibility:

    - `/basics/image`: The schema does not validate the field, so invalid values can be used, such
    as an empty string or a file path; here, only HTTP URLs are accepted.
    - `/basics/phone`: The schema does not impose a specific format for the phone number; here,
    RFC3966 is used.
    - date fields: The schema accepts any ISO 8601 string; here, only common ISO 8601 formats are
    accepted.

    There are also some other differences that are not mentioned because they are unlikely to break
    compatibility.
    """

    json_schema: Annotated[HttpUrl | None, AfterValidator(validate_json_schema_url)] = Field(
        alias="$schema",
        default=None,
        validate_default=True,
    )
    basics: JsonResumeBasics = Field(default_factory=JsonResumeBasics)
    work: list[JsonResumeWork] = Field(default_factory=list)
    volunteer: list[JsonResumeVolunteer] = Field(default_factory=list)
    education: list[JsonResumeEducation] = Field(default_factory=list)
    awards: list[JsonResumeAward] = Field(default_factory=list)
    certificates: list[JsonResumeCertificate] = Field(default_factory=list)
    publications: list[JsonResumePublication] = Field(default_factory=list)
    skills: list[JsonResumeSkill] = Field(default_factory=list)
    languages: list[JsonResumeLanguage] = Field(default_factory=list)
    interests: list[JsonResumeInterest] = Field(default_factory=list)
    references: list[JsonResumeReference] = Field(default_factory=list)
    projects: list[JsonResumeProject] = Field(default_factory=list)
    meta: JsonResumeMeta = Field(default_factory=JsonResumeMeta)
