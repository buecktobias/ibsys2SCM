import random
from collections import Counter

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from scs.core.db.graph.graph_node_orm import GraphNodeORM
from scs.core.db.item_models.produced_item_orm import ProducedItemORM
from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM


# Database connection setup


def populate_db_with_test_data(session: Session, id1: int, id2: int):
    """Populates the database with test data for items and demand forecasts."""
    # Define test items and demand forecast data

    session.query(GraphNodeORM).delete()
    session.query(ProducedItemORM).delete()
    session.query(DemandForecastItemORM).delete()
    test_items = [ProducedItemORM(id=id1), ProducedItemORM(id=id2)]
    test_demand_forecasts = [
            DemandForecastItemORM(item_id=id1, period=1, quantity=10),
            DemandForecastItemORM(item_id=id2, period=1, quantity=20),
            DemandForecastItemORM(item_id=id1, period=2, quantity=100),
            DemandForecastItemORM(item_id=id2, period=2, quantity=20),
    ]
    # Populate the database
    session.add_all(test_items)
    session.commit()
    session.add_all(test_demand_forecasts)


def test_populate_db_with_test_data(db_session: Session):
    """Tests if the database is populated with the correct test data."""
    id1 = random.randint(1, 100 ** 9)
    id2 = random.randint(1, 10 ** 9)
    populate_db_with_test_data(db_session, id1, id2)

    test_items = db_session.query(ProducedItemORM).all()
    assert len(test_items) == 2, "Expected 2 test items in the database."

    demand_forecasts = db_session.query(DemandForecastItemORM).all()
    assert len(demand_forecasts) == 4, "Expected 4 demand forecast items in the database."


def test_demand_forecast_retrieval(db_session: Session, engine: Engine):
    """Tests retrieval and validation of demand forecast data."""
    engine.begin()
    # Setup database with predefined test data
    id1 = random.randint(1, 10 ** 9)
    id2 = random.randint(1, 10 ** 9)
    populate_db_with_test_data(db_session, id1, id2)

    forecast_result = db_session.query(DemandForecastItemORM).all()
    # Fetch result and validate
    forecast_dict = {
            forecast.period: Counter({forecast.item_id: forecast.quantity for forecast in forecast_result})
            for forecast in forecast_result
    }
    print(forecast_dict)  # Print for debugging purposes
    expected_result = {
            1: Counter({id1: 10, id2: 20}),
            2: Counter({id1: 100, id2: 20}),
    }

    assert forecast_dict == expected_result, "Forecast data does not match the expected result."
