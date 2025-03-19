import networkx as nx
import pytest

from material.graph.nodes.graph_nodes import Item
from material.graph.production_graph.material_product_graph import MaterialProductGraph
from material.graph.sub_graph import SubGraph


def test_build_cycle_raises():
    graph = MaterialProductGraph()
    graph.add_node(Item.from_node_id("E1"))
    graph.add_node(Item.from_node_id("E2"))
    graph.nx_graph._add_edge("1", "2", weight=1)
    graph.nx_graph._add_edge("2", "1", weight=1)
    with pytest.raises(Exception):
        graph._validator.validate()


def test_subgraph_add_process_edges():
    graph = MaterialProductGraph()
    graph.add_node(Item.from_node_id("E1"))
    graph.add_node(Item.from_node_id("E2"))
    subgraph = SubGraph("group1", graph)
    process = subgraph.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"E1": 5},
        output_uid="E2",
    )
    assert process is not None, "Process node not added."
    assert graph.nx_graph.has_edge("E1", process.label)
    assert graph.nx_graph.has_edge(process.label, "E2")
    assert graph.nx_graph.edges[process.label, "E2"]["weight"] == 1
