
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.shared.infrastructure.database import get_session
from . import handler as list_read_handler
from .schemas import ListReadingParams, ReadingResponse

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/readings", response_model=list[ReadingResponse] )
def list_readings(params: Annotated[ListReadingParams, Query()], session: SessionDep):
    return list_read_handler.handle(session=session, params=params)
