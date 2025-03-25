from collections import Counter

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scs.db.models.base import Base
from scs.db.models.item import Item
from scs.db.models.mixins.periodic_item_quantity import PeriodicItemQuantity
from scs.db.models.models import DemandForecast, ProducedItem

DATABASE_URL = r"sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before any tests, then drop them when done."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session():
    """Provides a clean SQLAlchemy Session for each test."""
    with Session(engine) as session:
        yield session
        session.rollback()


def test_create_and_fetch_item(db_session: Session):
    items = [ProducedItem(id=1), ProducedItem(id=2)]
    demand_forecasts = [
            DemandForecast(item_id=1, period=1, quantity=10),
            DemandForecast(item_id=2, period=1, quantity=20),
            DemandForecast(item_id=1, period=2, quantity=100),
            DemandForecast(item_id=2, period=2, quantity=20),
    ]
    db_session.add_all(items)
    db_session.commit()
    db_session.add_all(demand_forecasts)
    db_session.commit()

    result = DemandForecast.get_periodic_item_quantity(db_session)
    print(result)

    assert result == PeriodicItemQuantity(
            {
                    1: Counter[Item]({ProducedItem(1): 10, ProducedItem(2): 20}),
                    2: Counter[Item]({ProducedItem(1): 100, ProducedItem(2): 20}),
            }
    )
