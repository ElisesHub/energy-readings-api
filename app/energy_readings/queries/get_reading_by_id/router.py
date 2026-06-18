from fastapi import APIRouter
from app.shared.infrastructure.database import SessionDep
from . import handler as get_readings_by_id_handler
from .schemas import ReadingResponse

router = APIRouter()


@router.get("/readings/{reading_id}", response_model=ReadingResponse)
def get_reading_by_id(reading_id: int, session: SessionDep):
    return get_readings_by_id_handler.handle(session, reading_id)
