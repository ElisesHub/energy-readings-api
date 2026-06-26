from typing import Annotated

from functools import lru_cache
from fastapi import Depends
from sqlmodel import Session, create_engine
from app.shared.infrastructure.settings import get_settings

@lru_cache
def get_engine():
    return create_engine(get_settings().database_url,
                         pool_pre_ping=True)


def get_db_session():
    with Session(get_engine()) as session:
        yield session


DbSession = Annotated[Session, Depends(get_db_session)]
