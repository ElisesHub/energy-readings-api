from datetime import datetime
from app.energy_readings.shared.energy_reading_type import EnergyReadingType
from pydantic import BaseModel, ConfigDict, model_validator, Field


class ListReadingParams(BaseModel):
    meter_id: str | None = None
    reading_type: EnergyReadingType | None = None
    date_from: datetime | None = Field(default=None, alias="from")
    date_to: datetime | None = Field(default=None, alias="to")
    limit: int = 10
    offset: int = 0

    # Runs after Pydantic has parsed and validated every individual field, and is called
    # automatically. Because the fields are already set, it can compare them against each
    # other (field validators only see one field). A raised error becomes a 422.
    @model_validator(mode="after")
    def validate_from_to(self):
        if(self.date_from is not None and self.date_to is not None) and self.date_from > self.date_to:
            raise ValueError("from must be before to")
        return self


class ReadingResponse(BaseModel):             # output shape
    model_config = ConfigDict(from_attributes=True) # Allows model_validate() to populate this schema from an ORM entity's attributes, not just a dict.

    id: int
    meter_id: str
    timestamp: datetime
    kwh: float
    reading_type: EnergyReadingType