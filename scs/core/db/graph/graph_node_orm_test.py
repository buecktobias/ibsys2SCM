from scs.core.db.graph.graph_node_orm import GraphNodeORM
from scs.core.db.item_models.produced_item_orm import ProducedItemORM


def test_insert_and_retrieve_graph_node(db_session):
    # Assign
    graph_node = ProducedItemORM(id=101)
    db_session.add(graph_node)
    db_session.commit()

    # Act
    retrieved_node = db_session.get(GraphNodeORM, graph_node.id)

    # Assert
    assert retrieved_node is not None
    assert retrieved_node.id == graph_node.id
    assert retrieved_node.type == ProducedItemORM.__tablename__
