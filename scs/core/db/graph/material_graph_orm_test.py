from sqlalchemy.orm import Session


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


from sqlalchemy.orm import Session

from scs.core.db.graph.material_graph_orm import MaterialGraphORM
from scs.core.db.process_models.process_orm import ProcessORM


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
    # noinspection PydanticTypeChecker
    assert len(fetched_parent.subgraphs) == 1, "Expected one child graph linked to the parent graph."
    assert fetched_parent.subgraphs[0].name == "Child Graph", "Child graph name does not match."


def test_material_graph_process_association(db_session: Session):
    """Tests if processes can be correctly associated with a material graph."""
    material_graph = MaterialGraphORM(name="Graph with Process")
    process = ProcessORM(graph=material_graph, workstation_id=1, process_duration_minutes=10, setup_duration_minutes=10)

    db_session.add(material_graph)
    db_session.add(process)
    db_session.commit()

    fetched_graph = db_session.query(MaterialGraphORM).filter_by(name="Graph with Process").one()
    # noinspection PydanticTypeChecker
    assert len(fetched_graph.processes) == 1, "Expected one process associated with the material graph."
    assert fetched_graph.processes[0].id == process.id, "Associated process ID does not match."
