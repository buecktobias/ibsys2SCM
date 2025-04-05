import logging
import os
from pathlib import Path
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from scs.core.db.base import Base


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG
    )


@pytest.fixture(scope="session")
def test_engine():
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///test.db")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, Any, None]:
    """Sets up the database tables before all tests and tears them down afterwards."""
    sqlite_path = "test.db"
    database_url = f"sqlite:///{sqlite_path}"
    engine: Engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()
    delete_test_db(sqlite_path)


def delete_test_db(path: Path | str):
    """Deletes the test.db file if it exists."""
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture(scope="session")
def db_session(engine) -> Generator[Session, Any, None]:
    """Provides a transaction-scoped SQLAlchemy session for each test."""
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def clean_db_session(engine):
    """Provides a transaction-scoped SQLAlchemy session for each test, but deletes all data after each test."""
    yield db_session
    db_session.rollback()
    db_session.query(Base).delete()
