import pytest
from sqlmodel import Session, create_engine, SQLModel

from material.db.config import DATABASE_URL
from material.db.models import Item, MaterialGraph, ItemType  # Import your ORM models

# Use your real database URL (Modify as needed)
engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure tables exist before tests run."""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)  # Cleanup after tests


@pytest.fixture
def db_session():
    """Provides a database session."""
    with Session(engine) as session:
        yield session
        session.rollback()  # Ensure clean state between tests


def test_create_and_fetch_item(db_session):
    """Test storing and retrieving an Item from the real database."""
    new_item = Item(item_id=999, item_type=ItemType.BOUGHT, base_price=10)
    db_session.add(new_item)
    db_session.commit()

    fetched_item = db_session.get(Item, 999)  # Retrieve item by ID
    assert fetched_item is not None
    assert fetched_item.base_price == 10

    # Clean up
    db_session.delete(fetched_item)
    db_session.commit()


def test_create_and_fetch_graph(db_session):
    """Test storing and retrieving a MaterialGraph from the real database."""
    new_graph = MaterialGraph(graph_id="RealGraph", name="Real DB Graph")
    db_session.add(new_graph)
    db_session.commit()

    fetched_graph = db_session.get(MaterialGraph, "RealGraph")  # Retrieve graph by ID
    assert fetched_graph is not None
    assert fetched_graph.name == "Real DB Graph"

    # Clean up
    db_session.delete(fetched_graph)
    db_session.commit()
