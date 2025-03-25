import logging

import pytest


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

    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def real_engine():
    from scs.db.config import engine
    yield engine
