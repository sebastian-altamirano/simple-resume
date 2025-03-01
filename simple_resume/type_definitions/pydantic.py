from __future__ import annotations

from collections.abc import Hashable
from datetime import datetime
from typing import Annotated, TypeVar

from pydantic import AfterValidator, Field
from pydantic import PastDatetime as PydanticPastDatetime

from simple_resume.helpers.dates import to_aware_datetime
from simple_resume.helpers.validation import validate_unique_list

DateTime = Annotated[
    datetime,
    AfterValidator(to_aware_datetime),
]

PastDateTime = Annotated[
    PydanticPastDatetime,
    AfterValidator(to_aware_datetime),
]


ListItemType = TypeVar("ListItemType", bound=Hashable)

UniqueList = Annotated[
    list[ListItemType],
    AfterValidator(validate_unique_list),
    Field(json_schema_extra={"uniqueItems": True}),
]
