from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator, Field, AliasGenerator
from pydantic.alias_generators import to_camel

from app.energy_readings.shared.energy_reading_type import EnergyReadingType


class DailyAggregateResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, # Allows model_validate() to populate this schema from an ORM entity's attributes, not just a dict.
        alias_generator=AliasGenerator(serialization_alias=to_camel) # ensures the properties will be exported as camel case instead of following the python naming convention
    )
    day: datetime
    reading_count: int
    total_kwh: float


class DailyAggregateParams(BaseModel):
    meter_id: str
    reading_type: EnergyReadingType
    date_from: datetime  = Field(alias="from")
    date_to: datetime = Field(alias="to")

    @model_validator(mode="after")
    def from_before_to(self):
        if self.date_from >= self.date_to:
            raise ValueError("'from' must be before 'to'")
        return self
