from datetime import date, datetime

from app.energy_readings.shared.energy_reading_type import EnergyReadingType
from pydantic import BaseModel, ConfigDict, model_validator, Field


class DailyAggregateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
