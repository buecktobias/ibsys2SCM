import pytest
from sqlalchemy.orm import Session

from scs.core.db.models.base import Base
from scs.core.db.models.item_models import BoughtItemORM, Item, ProducedItemORM
from scs.core.db.models.graph_models import MaterialGraphORM
from scs.core.db.models.ws_models import WorkstationORM


@pytest.fixture(scope="session", autouse=True)
def setup_database(test_engine):
    """Create all tables before any tests"""
    Base.metadata.create_all(test_engine)
    yield


@pytest.fixture
def db_session(test_engine):
    """Provides a clean SQLAlchemy Session for each test."""
    with Session(test_engine) as session:
        yield session
        session.rollback()


def test_create_and_fetch_item(db_session: Session):
    new_item = ProducedItemORM(id=999)
    db_session.add(new_item)
    db_session.commit()

    fetched = db_session.get(Item, 999)
    assert fetched is not None
    assert fetched.id == 999

    db_session.delete(fetched)
    db_session.commit()


def test_create_and_fetch_graph(db_session: Session):
    new_graph = MaterialGraphORM(id=123, name="Real DB Graph")
    db_session.add(new_graph)
    db_session.commit()

    fetched = db_session.get(MaterialGraphORM, 123)
    assert fetched is not None
    assert isinstance(fetched, MaterialGraphORM)
    assert fetched.name == "Real DB Graph"

    db_session.delete(fetched)
    db_session.commit()


@pytest.fixture
def db(test_engine):
    with Session(test_engine) as session:
        yield session
        session.rollback()


def test_workstation(db: Session):
    ws = WorkstationORM(
            id=101,
            labour_cost_1=10, labour_cost_2=11, labour_cost_3=12,
            labour_overtime_cost=15, variable_machine_cost=20, fixed_machine_cost=30
    )
    db.add(ws)
    db.commit()
    assert db.get(WorkstationORM, ws.id)


def test_item_bought_produced(db: Session):
    produced = ProducedItemORM(id=1002207)
    db.add(produced)
    db.commit()

    bought = BoughtItemORM(
            id=101207, base_price=100.0, discount_amount=10,
            mean_order_duration=3.0, order_std_dev=0.5, base_order_cost=25.0
    )
    db.add_all([bought, produced])
    db.commit()

    assert db.get(BoughtItemORM, bought.id)
    assert db.get(ProducedItemORM, produced.id)
