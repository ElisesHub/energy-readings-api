
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.shared.infrastructure.database import get_session
from . import handler as get_readings_by_id_handler
from .schemas import ReadingResponse

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/readings/{reading_id}", response_model=ReadingResponse)
def get_reading_by_id(reading_id: int, session: SessionDep):
    return get_readings_by_id_handler.handle(session=session, reading_id=reading_id)