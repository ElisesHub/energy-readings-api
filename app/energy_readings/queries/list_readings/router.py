from typing import Annotated
from fastapi import APIRouter, Query
from app.shared.infrastructure.database import SessionDep
from . import handler as list_read_handler
from .schemas import ListReadingParams, ReadingResponse

router = APIRouter()


@router.get("/readings", response_model=list[ReadingResponse])
def list_readings(params: Annotated[ListReadingParams, Query()], session: SessionDep):
    return list_read_handler.handle(session, params)
