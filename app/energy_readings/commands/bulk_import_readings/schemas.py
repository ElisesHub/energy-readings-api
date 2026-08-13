from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel

from app.energy_readings.shared.energy_reading_type import EnergyReadingType


class SingleReading(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # Allows model_validate() to populate this schema from an ORM entity's attributes, not just a dict.
        alias_generator=AliasGenerator(serialization_alias=to_camel)
        # ensures the properties will be exported as camel case instead of following the python naming convention
    )

    meter_id: str
    timestamp: datetime
    kwh: float
    reading_type: EnergyReadingType

    @field_validator("kwh")
    @classmethod
    def kwh_validator(cls, v):
        if v < 0:
            raise ValueError("'kwh' must be greater than 0")
        return v


class BulkCreateResponse(BaseModel):
    success_count: int
    failure_count: int
    errors: List[BulkImportError]


class BulkImportError(BaseModel):
        reading: SingleReading  # the input that failed
        error: str