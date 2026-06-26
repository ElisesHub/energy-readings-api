import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session

from app.main import app
from app.shared.infrastructure.database import get_db_session  # the real db dependency, overridden in tests

dotenv_path = Path(__file__).parent / ".env.test"
load_dotenv(dotenv_path=dotenv_path, override=True)

# os.environ[...] fails fast if a variable is missing — required config
db_username = os.environ["TEST_POSTGRES_USERNAME"]
db_password = os.environ["TEST_POSTGRES_PASSWORD"]
db_name = os.environ["TEST_DB_REF"]
db_host = os.environ["TEST_POSTGRES_HOST"]
# os.getenv returns the default if the variable is missing — optional config
db_port = os.getenv("TEST_POSTGRES_PORT", "5445")

TEST_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Engine = SQLAlchemy's connection pool + dialect handler for the test database
test_db_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Opens a transaction per test and rolls it back at the end — keeps tests isolated."""
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def http_client(db_session: Session) -> Generator[TestClient, None, None]:
    """Fake HTTP client routed through the app, with the test db session wired in."""
    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()