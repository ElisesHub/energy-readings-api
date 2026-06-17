
from sqlmodel import Session, select
from fastapi import HTTPException
from app.energy_readings.shared.energy_reading import EnergyReading


def handle(session: Session, reading_id: int) -> EnergyReading:
    reading = session.exec(
        select(EnergyReading).where(EnergyReading.id == reading_id)
    ).first()
    if reading is None:
        raise HTTPException(status_code=404, detail=f"Reading {reading_id} not found")
    return reading