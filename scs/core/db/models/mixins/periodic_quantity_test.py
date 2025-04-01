from collections import Counter
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from scs.core.db.models.base import Base
from scs.core.db.models.item_models.produced_item_orm import ProducedItemORM
from scs.core.db.models.periodic.demand_forecast_item_orm import DemandForecastItemORM
from scs.core.domain.periodic_item_quantities import PeriodicItemQuantity

# Database connection setup
DATABASE_URL = r"sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Sets up the database tables before all tests and tears them down afterwards."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()
    delete_test_db()


def delete_test_db():
    """Deletes the test.db file if it exists."""
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def db_session():
    """Provides a transaction-scoped SQLAlchemy session for each test."""
    with Session(engine) as session:
        yield session
        session.rollback()


def populate_db_with_test_data(session: Session):
    """Populates the database with test data for items and demand forecasts."""
    # Define test items and demand forecast data
    test_items = [ProducedItemORM(id=1), ProducedItemORM(id=2)]
    test_demand_forecasts = [
            DemandForecastItemORM(item_id=1, period=1, quantity=10),
            DemandForecastItemORM(item_id=2, period=1, quantity=20),
            DemandForecastItemORM(item_id=1, period=2, quantity=100),
            DemandForecastItemORM(item_id=2, period=2, quantity=20),
    ]
    # Populate the database
    session.add_all(test_items)
    session.commit()
    session.add_all(test_demand_forecasts)
    session.commit()


def test_populate_db_with_test_data(db_session: Session):
    """Tests if the database is populated with the correct test data."""
    populate_db_with_test_data(db_session)

    test_items = db_session.query(ProducedItemORM).all()
    assert len(test_items) == 2, "Expected 2 test items in the database."

    demand_forecasts = db_session.query(DemandForecastItemORM).all()
    assert len(demand_forecasts) == 4, "Expected 4 demand forecast items in the database."


def test_demand_forecast_retrieval(db_session: Session):
    """Tests retrieval and validation of demand forecast data."""
    # Setup database with predefined test data
    populate_db_with_test_data(db_session)

    # Fetch result and validate
    forecast_result = db_session.query(DemandForecastItemORM).all()
    forecast_dict = {
            forecast.period: Counter({forecast.item_id: forecast.quantity for forecast in forecast_result})
            for forecast in forecast_result
    }
    print(forecast_dict)  # Print for debugging purposes
    expected_result = {
            1: Counter({1: 10, 2: 20}),
            2: Counter({1: 100, 2: 20}),
    }

    assert forecast_dict == expected_result, "Forecast data does not match the expected result."
