from collections import Counter

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scs.core.db.models.base import Base
from scs.core.db.models.item_models import ItemORM, ProducedItemORM
from scs.core.domain.periodic_item_quantities import PeriodicItemQuantity
from scs.core.db.models.periodic.demand_model import DemandForecastORM

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
    items = [ProducedItemORM(id=1), ProducedItemORM(id=2)]
    demand_forecasts = [
            DemandForecastORM(item_id=1, period=1, quantity=10),
            DemandForecastORM(item_id=2, period=1, quantity=20),
            DemandForecastORM(item_id=1, period=2, quantity=100),
            DemandForecastORM(item_id=2, period=2, quantity=20),
    ]
    db_session.add_all(items)
    db_session.commit()
    db_session.add_all(demand_forecasts)
    db_session.commit()

    result = DemandForecastORM.get_forecast_starting_with(db_session)
    print(result)

    assert result == PeriodicItemQuantity(
            {
                    1: Counter[ItemORM]({ProducedItemORM(1): 10, ProducedItemORM(2): 20}),
                    2: Counter[ItemORM]({ProducedItemORM(1): 100, ProducedItemORM(2): 20}),
            }
    )
