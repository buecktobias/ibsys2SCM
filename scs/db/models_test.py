import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scs.db.models.base import Base
from scs.db.models.item import Item
from scs.db.models.models import BoughtItem, MaterialGraphORM, ProducedItem, Workstation

DATABASE_URL = r"sqlite:///test.db"
engine = create_engine(DATABASE_URL, echo=True)


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
    new_item = Item(id=999)
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
def db():
    with Session(engine) as session:
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
    db.commit()

    bought = BoughtItem(
            id=10001207, base_price=100.0, discount_amount=10,
            mean_order_duration=3.0, order_std_dev=0.5, base_order_cost=25.0
    )
    produced = ProducedItem(id=2223)
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
