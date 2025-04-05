from sqlalchemy.orm import Session

from scs.core.db.item_models.bought_item_orm import BoughtItemORM
from scs.core.db.item_models.item_orm import ItemORM
from scs.core.db.item_models.produced_item_orm import ProducedItemORM


def test_create_and_fetch_item(db_session: Session):
    new_item = ProducedItemORM(id=999)
    db_session.add(new_item)
    db_session.commit()

    fetched = db_session.get(ItemORM, 999)
    assert fetched is not None
    assert fetched.id == 999

    db_session.delete(fetched)
    db_session.commit()


def test_item_bought_produced(db_session: Session):
    produced = ProducedItemORM(id=1002207)
    db_session.add(produced)
    db_session.commit()

    bought = BoughtItemORM(
            id=101207, base_price=100.0, discount_amount=10,
            mean_order_duration=3.0, order_std_dev=0.5, base_order_cost=25.0
    )
    db_session.add_all([bought, produced])
    db_session.commit()

    assert db_session.get(BoughtItemORM, bought.id)
    assert db_session.get(ProducedItemORM, produced.id)
