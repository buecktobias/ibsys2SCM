from scs.core.db.periodic.inventory_item_orm import InventoryItemORM


def test_inventory_item_orm_table_name():
    assert InventoryItemORM.__tablename__ == "inventory"


def test_inventory_item_orm_inherits_base():
    from scs.core.db.base import Base
    assert issubclass(InventoryItemORM, Base)


def test_inventory_item_orm_inherits_period_mixin():
    from scs.core.db.mixins.period_mixin import PeriodMixin
    assert issubclass(InventoryItemORM, PeriodMixin)


def test_inventory_item_orm_period_column(db_session):
    # Assign
    inventory_item = InventoryItemORM(period=5)

    # Act
    db_session.add(inventory_item)
    db_session.commit()

    # Assert
    fetched_item = db_session.query(InventoryItemORM).filter_by(period=5).first()
    assert fetched_item is not None
    assert fetched_item.period == 5
