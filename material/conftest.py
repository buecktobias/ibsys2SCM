import logging
import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG
    )
