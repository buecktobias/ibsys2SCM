from sqlalchemy.orm import Session

from scs.core.db.graph.material_graph_orm import MaterialGraphORM


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
