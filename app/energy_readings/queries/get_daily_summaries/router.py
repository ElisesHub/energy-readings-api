from typing import Annotated, List
from fastapi import APIRouter, Query
from app.shared.infrastructure.database import DbSession
from . import handler as daily_summaries_handler
from .schemas import DailySummaryResponse, DailySummaryParams

router = APIRouter()


@router.get("/summaries/daily", response_model=List[DailySummaryResponse])
def get_daily_readings(params: Annotated[DailySummaryParams, Query()], session: DbSession):
    return daily_summaries_handler.handle(session, params)
