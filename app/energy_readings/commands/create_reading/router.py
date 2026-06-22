from typing import Annotated
from fastapi import APIRouter,  Body
from .schemas import CreateReadingResponse, ParamsCreateReading
from app.shared.infrastructure.database import SessionDep
from . import handler as create_reading_handler

router = APIRouter()

@router.post("/readings", response_model=CreateReadingResponse, status_code=201)
def create_reading_router(params: Annotated[ParamsCreateReading, Body()], session: SessionDep):

    return create_reading_handler.handle(session, params)