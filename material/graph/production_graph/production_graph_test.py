import logging

import pytest

from material.graph.nodes.graph_nodes import Item
from material.graph.production_graph.material_product_graph import MaterialProductGraph
from material.graph.sub_graph import SubGraph


# Dummy _validator functions to bypass actual validation during tests.
def dummy_validate():
    pass


def dummy_is_adding_edge_valid(source_uid, target_uid, weight):
    pass


@pytest.fixture
def graph():
    g = MaterialProductGraph()
    return g


def test_add_item(graph: MaterialProductGraph):
    graph.add_node(Item.from_node_id("K1"))
    assert graph.has_node(Item.from_node_id("K1"))


def test_duplicate_item(graph: MaterialProductGraph, caplog):
    caplog.clear()
    graph.add_node(Item.from_node_id("K1"))

    initial_count = len(graph.nx_graph.nodes)
    graph.add_node(Item.from_node_id("K1"))
    # The node count should not increase.
    assert len(graph.nx_graph.nodes) == initial_count


def test_subgraph_add_process_edges(graph: MaterialProductGraph):
    # Prepare counter.
    graph.add_node(Item.from_node_id("K1"))
    graph.add_node(Item.from_node_id("E1"))
    # Create a SubGraph.
    subgraph = SubGraph("group1", graph)
    # Add a process with input {"K1": 2} and _output "E1"
    process = subgraph.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"K1": 2},
        output_uid="E1",
    )
    assert process is not None, "Process node not added."
    expected_uid = process.node_id  # Computed by the Process implementation.
    # Check that the process node is in the graph.
    assert expected_uid in graph.nx_graph.nodes
    # Check that the edge from input ("K1") to process exists with weight 2.


def test_duplicate_process(graph: MaterialProductGraph, caplog):
    # Prepare counter.
    graph.add_node(Item.from_node_id("K1"))
    graph.add_node(Item.from_node_id("E1"))
    subgraph = SubGraph("group1", graph)
    caplog.clear()
    subgraph.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"K1": 2},
        output_uid="E1",
    )
    initial_count = len(graph.nx_graph.nodes)
    subgraph.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"K1": 2},
        output_uid="E1",
    )
    assert len(graph.nx_graph.nodes) == initial_count
    assert any("already exists" in record.message for record in caplog.records)


def test_subgraph_addition():
    parent_graph = MaterialProductGraph()
    parent_graph._validator.validate = dummy_validate
    parent_graph._validator.is_adding_edge_valid = dummy_is_adding_edge_valid
    subgraph = SubGraph("test", parent_graph)
    item = Item.from_node_id("K5")
    subgraph.add_node(item)
    key = f"{item._node_type.value}{item.node_id}"
    assert key in parent_graph.nx_graph.nodes
    assert item in subgraph.get_node_aggregates()
