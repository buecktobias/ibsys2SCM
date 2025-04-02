import pytest
from scs.core.db.models.base import Base
from scs.core.db.models.graph.material_graph_orm import MaterialGraphORM
from scs.core.db.models.process_models.process_orm import ProcessORM
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture
def db_session():
    """Fixture to set up an in-memory database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_material_graph_creation(db_session: Session):
    """Tests if a MaterialGraphORM object can be successfully created and added to the database."""
    material_graph = MaterialGraphORM(name="Test Graph")
    db_session.add(material_graph)
    db_session.commit()

    fetched_graphs = db_session.query(MaterialGraphORM).all()
    assert len(fetched_graphs) == 1, "Expected one material graph in the database."
    assert fetched_graphs[0].name == "Test Graph", "Material graph name does not match."


def test_material_graph_hierarchy(db_session: Session):
    """Tests if hierarchical relationships between material graphs are correctly handled."""
    parent_graph = MaterialGraphORM(name="Parent Graph")
    child_graph = MaterialGraphORM(name="Child Graph", parent_graph=parent_graph)

    db_session.add(parent_graph)
    db_session.add(child_graph)
    db_session.commit()

    fetched_parent = db_session.query(MaterialGraphORM).filter_by(name="Parent Graph").one()
    assert len(fetched_parent.subgraphs) == 1, "Expected one child graph linked to the parent graph."
    assert fetched_parent.subgraphs[0].name == "Child Graph", "Child graph name does not match."


def test_material_graph_process_association(db_session: Session):
    """Tests if processes can be correctly associated with a material graph."""
    material_graph = MaterialGraphORM(name="Graph with Process")
    process = ProcessORM(graph=material_graph)

    db_session.add(material_graph)
    db_session.add(process)
    db_session.commit()

    fetched_graph = db_session.query(MaterialGraphORM).filter_by(name="Graph with Process").one()
    assert len(fetched_graph.processes) == 1, "Expected one process associated with the material graph."
    assert fetched_graph.processes[0].id == process.id, "Associated process ID does not match."
