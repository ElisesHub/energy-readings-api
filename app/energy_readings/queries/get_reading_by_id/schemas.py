from datetime import datetime
from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel

from app.energy_readings.shared.energy_reading_type import EnergyReadingType


class ReadingResponse(BaseModel):             # output shape
    model_config = ConfigDict(
        from_attributes=True,  # Allows model_validate() to populate this schema from an ORM entity's attributes, not just a dict.
        alias_generator=AliasGenerator(serialization_alias=to_camel)
        # ensures the properties will be exported as camel case instead of following the python naming convention
    )
    id: int
    meter_id: str
    timestamp: datetime
    kwh: float
    reading_type: EnergyReadingType

