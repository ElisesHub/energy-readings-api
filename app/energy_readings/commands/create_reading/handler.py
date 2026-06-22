from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.energy_readings.commands.create_reading.schemas import ParamsCreateReading, CreateReadingResponse
from app.energy_readings.shared.energy_reading import EnergyReading


def handle(session: Session, params: ParamsCreateReading) -> CreateReadingResponse:

    db_reading = EnergyReading.model_validate(params)
    session.add(db_reading)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Reading already exists for this meter, hour and type")
    session.refresh(db_reading)
    return db_reading