from sqlalchemy import DateTime
from app.energy_readings.shared.energy_reading_type import EnergyReadingType
from sqlmodel import Column
from sqlmodel import Field, SQLModel, Enum as SAEnum
import datetime

class EnergyReading(SQLModel, table=True):
    __tablename__ = "energy_reading"
    id: int | None = Field(default=None, primary_key=True)
    meter_id: str
    timestamp: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    age: float | None = Field(default=None, index=True)
    reading_type: EnergyReadingType = Field(
        sa_column=Column(
            SAEnum(
                EnergyReadingType,
                values_callable=lambda x: [e.value for e in x],
                native_enum=False,
            ),
            nullable=False,
        )
    )


