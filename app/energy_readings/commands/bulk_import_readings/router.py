from typing import Annotated, List
from fastapi import APIRouter,  Body
from app.shared.infrastructure.database import DbSession
from . import handler as create_bulk_reading_handler
from .schemas import BulkCreateResponse, SingleReading

router = APIRouter()

@router.post("/readings/bulk", response_model=BulkCreateResponse, status_code=201)
def bulk_import_readings_router(params: Annotated[List[SingleReading], Body()], session: DbSession):

    return create_bulk_reading_handler.handle(session, params)