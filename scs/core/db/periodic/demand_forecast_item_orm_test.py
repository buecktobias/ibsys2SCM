import pytest

from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM


def test_demand_forecast_item_orm_table_name():
    assert DemandForecastItemORM.__tablename__ == "demand_forecast"


def test_demand_forecast_item_orm_period_column():
    # Arrange, Act
    instance = DemandForecastItemORM()

    # Assert
    assert hasattr(instance, 'period'), "Attribute 'period' is not present in the ORM model."


def test_demand_forecast_item_orm_quantity_column():
    # Arrange, Act
    instance = DemandForecastItemORM()

    # Assert
    assert hasattr(instance, 'quantity'), "Attribute 'quantity' is not present in the ORM model."


@pytest.mark.usefixtures("db_session")
def test_demand_forecast_item_orm_inserts_to_db(db_session):
    # Arrange
    instance = DemandForecastItemORM(period=202310, item_id=1001, quantity=50)

    # Act
    db_session.add(instance)
    db_session.commit()
    result = db_session.query(DemandForecastItemORM).filter_by(period=202310).one()

    # Assert
    assert result.period == 202310
    assert result.item_id == 1001
    assert result.quantity == 50
