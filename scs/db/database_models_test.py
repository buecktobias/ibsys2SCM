import pytest
from sqlalchemy.orm import Session

from scs.db.models.base import Base
from scs.db.models.item import Item
from scs.db.models.models import BoughtItem, MaterialGraphORM, ProducedItem, Workstation


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
    new_item = ProducedItem(id=999)
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
    ws = Workstation(
            id=101,
            labour_cost_1=10, labour_cost_2=11, labour_cost_3=12,
            labour_overtime_cost=15, variable_machine_cost=20, fixed_machine_cost=30
    )
    db.add(ws)
    db.commit()
    assert db.get(Workstation, ws.id)


def test_item_bought_produced(db: Session):
    produced = ProducedItem(id=1002207)
    db.add(produced)
    db.commit()

    bought = BoughtItem(
            id=101207, base_price=100.0, discount_amount=10,
            mean_order_duration=3.0, order_std_dev=0.5, base_order_cost=25.0
    )
    db.add_all([bought, produced])
    db.commit()

    assert db.get(BoughtItem, bought.id)
    assert db.get(ProducedItem, produced.id)


def test_material_graph_hierarchy(db: Session):
    root = MaterialGraphORM(id=10008, name="Root")
    child = MaterialGraphORM(id=1000097, name="Child", parent_graph=root)
    db.add_all([root, child])
    db.commit()

    assert child.parent_graph == root
    assert root.subgraphs == [child]
