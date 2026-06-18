from sqlalchemy.sql.functions import func
from sqlmodel import Session, select
from fastapi import HTTPException
from app.energy_readings.shared.energy_reading import EnergyReading
from .schemas import DailyAggregateParams



def handle(session: Session, params: DailyAggregateParams):

    day = func.date_trunc("day", EnergyReading.timestamp).label("day")
    reading_count = func.count(EnergyReading.id).label("reading_count")
    aggregate_kwh = func.sum(EnergyReading.kwh).label("total_kwh")

    query = select(aggregate_kwh, day, reading_count)

    query = query.where(
        EnergyReading.meter_id == params.meter_id,
        EnergyReading.reading_type == params.reading_type,
        EnergyReading.timestamp >= params.date_from,
        EnergyReading.timestamp < params.date_to)

    query = query.group_by(day)


    result = session.exec(query).all()

    return result
