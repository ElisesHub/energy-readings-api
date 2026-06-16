from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
from app.shared.infrastructure.settings import get_settings

engine = create_engine(get_settings().database_url)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]