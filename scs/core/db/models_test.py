import pytest
from sqlalchemy.orm import Session

from scs.core.db.models.base import Base
from scs.core.db.models.item_models import BoughtItemORM, ItemORM, ProducedItemORM
from scs.core.db.models.graph_models import MaterialGraphORM
from scs.core.db.models.ws_models import WorkstationORM


@pytest.fixture(scope="session", autouse=True)
def setup_database(test_engine):
    """Create all tables before any tests, then drop them when done."""
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Provides a clean SQLAlchemy Session for each test."""
    with Session(test_engine) as session:
        yield session
        session.rollback()


def test_create_and_fetch_item(db_session: Session):
    new_item = ItemORM(id=999)
    db_session.add(new_item)
    db_session.commit()

    fetched = db_session.get(ItemORM, 999)
    assert fetched is not None
    assert fetched.id == 999

    db_session.delete(fetched)
    db_session.commit()


def test_workstation(db_session: Session):
    ws = WorkstationORM(
            id=11101,
            labour_cost_1=10, labour_cost_2=11, labour_cost_3=12,
            labour_overtime_cost=15, variable_machine_cost=20, fixed_machine_cost=30
    )
    db_session.add(ws)
    db_session.commit()
    assert db_session.get(WorkstationORM, ws.id)


def test_item_bought_produced(db_session: Session):
    db_session.commit()

    bought = BoughtItemORM(
            id=10001207, base_price=100.0, discount_amount=10,
            mean_order_duration=3.0, order_std_dev=0.5, base_order_cost=25.0
    )
    produced = ProducedItemORM(id=2223)
    db_session.add_all([bought, produced])
    db_session.commit()

    assert db_session.get(BoughtItemORM, bought.id)
    assert db_session.get(ProducedItemORM, produced.id)


def test_material_graph_hierarchy(db_session: Session):
    root = MaterialGraphORM(id=10008, name="Root")
    child = MaterialGraphORM(id=1000097, name="Child", parent_graph=root)
    db_session.add_all([root, child])
    db_session.commit()

    assert child.parent_graph == root
    assert root.subgraphs == [child]
