import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from material.db.models import Base, MaterialGraph, Item

DATABASE_URL = r"postgresql+psycopg://postgres:secret@localhost:6543/postgres"
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
    new_graph = MaterialGraph(id=123, name="Real DB Graph")
    db_session.add(new_graph)
    db_session.commit()

    fetched = db_session.get(MaterialGraph, 123)
    assert fetched is not None
    assert isinstance(fetched, MaterialGraph)
    assert fetched.name == "Real DB Graph"

    db_session.delete(fetched)
    db_session.commit()
