from typing import Annotated, List
from fastapi import APIRouter, Query
from app.shared.infrastructure.database import SessionDep
from . import handler as daily_aggregates_handler
from .schemas import DailyAggregateResponse, DailyAggregateParams

router = APIRouter()


@router.get("/aggregates/daily", response_model=List[DailyAggregateResponse])
def get_daily_readings(params: Annotated[DailyAggregateParams, Query()], session: SessionDep):
    return daily_aggregates_handler.handle(session, params)
