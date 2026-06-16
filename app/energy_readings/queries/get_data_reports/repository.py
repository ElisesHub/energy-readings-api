# app/energy_readings/queries/get_data_reports/repository.py
from sqlmodel import Session, select

from app.energy_readings.shared.energy_reading import EnergyReading


class EnergyReadingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self) -> list[EnergyReading]:
        return list(self._session.exec(select(EnergyReading)).all())