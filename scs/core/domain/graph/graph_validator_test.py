import networkx as nx
import pytest

from scs.core.domain.graph.edge_models import ProcessInputEdge
from scs.core.domain.graph.graph_validator import GraphValidator
from scs.core.domain.production_graph import ProductionGraph


@pytest.fixture
def simple_graph(item_factory):
    # Nodes
    nodes = {
            1: item_factory.create_produced_item(id=1),
            2: item_factory.create_produced_item(id=2),
            3: item_factory.create_produced_item(id=3)
    }

    # Graph
    g = nx.DiGraph()
    g.add_edge(1, 2, weight=1)
    g.add_edge(2, 3, weight=1)

    return ProductionGraph(g, nodes)


def test_no_cycle_valid(simple_graph):
    validator = GraphValidator(simple_graph)
    validator.validate()  # Should not raise


def test_cycle_detection(item_factory):
    g = nx.DiGraph()
    g.add_edge(1, 2, weight=1)
    g.add_edge(2, 3, weight=1)
    g.add_edge(3, 1, weight=1)

    nodes = {i: item_factory.create_produced_item(i) for i in [1, 2, 3]}
    graph = ProductionGraph(g, nodes)

    validator = GraphValidator(graph)

    with pytest.raises(ValueError):
        validator.validate()


def test_isolated_node_detection(item_factory):
    g = nx.DiGraph()
    g.add_edge(1, 2)
    g.add_node(3)  # isolated

    nodes = {i: item_factory.create_produced_item(i) for i in [1, 2, 3]}
    graph = ProductionGraph(g, nodes)

    validator = GraphValidator(graph)

    with pytest.raises(ValueError):
        validator.validate()


def test_invalid_out_degree(monkeypatch, item_factory):
    g = nx.DiGraph()
    g.add_edge(1, 2, weight=1)
    g.add_edge(1, 3, weight=1)  # node 1 has two outgoing edges

    nodes = {i: item_factory.create_produced_item(i) for i in [1, 2, 3]}
    graph = ProductionGraph(g, nodes)

    # Patch edges to simulate ProcessInputEdge
    # noinspection PyUnusedLocal
    @property
    def mock_edges(self):
        return [ProcessInputEdge(from_node=nodes[1], to_node=nodes[2], weight=1)]

    monkeypatch.setattr(ProductionGraph, "edges", mock_edges)

    validator = GraphValidator(graph)

    with pytest.raises(RuntimeError):
        validator.validate()
