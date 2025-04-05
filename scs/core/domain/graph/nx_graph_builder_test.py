from scs.conftest import item_factory
from scs.core.domain.graph.nx_graph_builder import NxGraphBuilder


def test_add_edge_adds_nodes_and_edge(process_factory, item_factory):
    builder = NxGraphBuilder()
    node_a = item_factory.create_produced_item(id=1)
    node_b = item_factory.create_produced_item(id=2)

    builder._add_edge(node_a, node_b, weight=5)

    assert node_a.id in builder.graph.nodes
    assert node_b.id in builder.graph.nodes
    assert builder.graph.has_edge(1, 2)
    assert builder.graph.edges[1, 2]["weight"] == 5


def test_build_from_database_creates_correct_graph(process_factory, item_factory):
    input_node = item_factory.create_produced_item(id=10)
    output_node = item_factory.create_produced_item(30)
    process_node = process_factory.create(id=20, inputs={input_node: 3}, output=output_node)

    builder = NxGraphBuilder()
    graph = builder.build_from_processes([process_node])

    assert input_node.id in graph.nodes
    assert process_node.id in graph.nodes
    assert output_node.id in graph.nodes

    assert graph.has_edge(10, 20)
    assert graph.edges[10, 20]["weight"] == 3

    assert graph.has_edge(20, 30)
    assert graph.edges[20, 30]["weight"] == 1
