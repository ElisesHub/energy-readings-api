from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator, ConfigDict

from app.energy_readings.shared.energy_reading_type import EnergyReadingType


class SingleReading(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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