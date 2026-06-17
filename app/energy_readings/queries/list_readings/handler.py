
from sqlmodel import Session, select
from app.energy_readings.shared.energy_reading import EnergyReading
from .schemas import ListReadingParams
from fastapi import HTTPException

def handle(session: Session, params: ListReadingParams) -> list[EnergyReading]:
    query = select(EnergyReading)

    if params.meter_id is not None:
        query = query.where(EnergyReading.meter_id == params.meter_id)
    if params.reading_type is not None:
        query = query.where(EnergyReading.reading_type == params.reading_type)
    if params.date_from is not None:
        query = query.where(EnergyReading.timestamp >= params.date_from)
    if params.date_to is not None:
        query = query.where(EnergyReading.timestamp < params.date_to)

    query = query.order_by(EnergyReading.timestamp, EnergyReading.meter_id)
    query = query.offset(params.offset).limit(params.limit)

    result =  session.exec(query).all()   # entities — FastAPI converts them

    if result is None or len(result) == 0:
        raise HTTPException(status_code=404, detail=f"Empty list returned")
    return result