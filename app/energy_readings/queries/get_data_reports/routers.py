# app/energy_readings/queries/get_data_reports/routers.py
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.shared.infrastructure.database import get_session
from app.energy_readings.queries.get_data_reports.repository import EnergyReadingRepository

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]

def get_energy_reading_repository(session: SessionDep) -> EnergyReadingRepository:
    return EnergyReadingRepository(session)


RepositoryDep = Annotated[EnergyReadingRepository, Depends(get_energy_reading_repository)]


@router.get("/reports")
def get_data_reports(repository: RepositoryDep):
    return repository.get_all()