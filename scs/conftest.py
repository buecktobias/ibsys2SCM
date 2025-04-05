import logging
import os
import random
from pathlib import Path
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from scs.core.db.base import Base
from scs.core.db.item_models.produced_item_orm import ProducedItemORM
from scs.tests.item_factory import ItemFactory
from scs.tests.process_factory import ProcessFactory
from scs.tests.workstation_factory import WorkstationFactory


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


@pytest.fixture(scope="session")
def random_produced_item():
    return ProducedItemORM(id=random.randint(1, 10 ** 8))


@pytest.fixture(scope="session")
def item_factory():
    return ItemFactory()


@pytest.fixture(scope="session")
def workstation_factory():
    return WorkstationFactory()


@pytest.fixture(scope="session")
def process_factory(item_factory, workstation_factory):
    return ProcessFactory(
            item_factory=item_factory,
            workstation_factory=workstation_factory
    )
