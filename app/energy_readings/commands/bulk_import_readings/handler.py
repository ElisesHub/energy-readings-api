from typing import List

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.energy_readings.shared.energy_reading import EnergyReading
from .schemas import BulkCreateResponse, BulkImportError, SingleReading




def handle(session: Session, params: List[SingleReading]) -> BulkCreateResponse:

    success_count: int = 0
    failure_count: int = 0
    errors: List[BulkImportError] = []

    for reading in params:
        try:
            with session.begin_nested():
                db_reading = EnergyReading.model_validate(reading)
                session.add(db_reading)
        except IntegrityError:
            failure_count += 1
            errors.append(BulkImportError(
                reading = reading,
                error = F'The {reading.reading_type} reading is already stored for meter: {reading.meter_id} at {reading.timestamp}'
                )
             )
        else:
            success_count += 1

    session.commit()

    return BulkCreateResponse(
        success_count = success_count,
        failure_count = failure_count,
        errors = errors
    )
