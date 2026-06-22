from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.energy_readings.shared.energy_reading_type import EnergyReadingType


class ReadingResponse(BaseModel):             # output shape
    model_config = ConfigDict(from_attributes=True) # Allows model_validate() to populate this schema from an ORM entity's attributes, not just a dict.
    id: int
    meter_id: str
    timestamp: datetime
    kwh: float
    reading_type: EnergyReadingType

