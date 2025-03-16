import pytest
import networkx as nx
import logging

from material.graph.graph_nodes import Item, Process, GraphNode
from material.graph.production_graph_validator import GraphValidator
from material.graph.material_product_flow_graph import (
    GraphBuilder,
    BuilderSubgraph,
    MaterialProductFlowGraph,
    SubGraph,
    BaseGraph,
)


# Dummy validator functions to bypass actual validation during tests.
def dummy_validate():
    pass


def dummy_is_adding_edge_valid(source_uid, target_uid, weight):
    pass


@pytest.fixture
def builder():
    builder = GraphBuilder()
    # Override the validator methods to always pass.
    builder.graph.validator.validate = dummy_validate
    builder.graph.validator.is_adding_edge_valid = dummy_is_adding_edge_valid
    return builder


def test_add_item(builder):
    # Test that adding an item registers it in the builder's material_map and graph.
    builder.add_item("K1")
    # For "K1", Item.from_node_id returns an Item with node_id == 1, so node_uid == "1"
    assert "K1" in builder.material_map
    item = builder.material_map["K1"]
    assert item.node_uid == "1"
    # The graph should contain the node with uid "1"
    assert "1" in builder.graph.graph.nodes


def test_get_or_add(builder):
    # Test that get_or_add returns the same node on repeated calls.
    node1 = builder.get_or_add("K1")
    node2 = builder.get_or_add("K1")
    assert node1 is node2
    # The node should be in the material_map and graph.
    assert "K1" in builder.material_map
    assert node1.node_uid in builder.graph.graph.nodes


def test_duplicate_item(builder, caplog):
    # Test that adding the same item twice does not create duplicates.
    caplog.clear()
    builder.add_item("K1")
    initial_count = len(builder.graph.graph.nodes)
    builder.add_item("K1")  # Attempt to add duplicate.
    # The node count should not increase.
    assert len(builder.graph.graph.nodes) == initial_count
    # A warning should be logged.
    assert any("already exists" in record.message for record in caplog.records)


def test_builder_subgraph_add_process(builder):
    # Prepare items.
    builder.add_item("K1")
    builder.add_item("E1")
    # Create a BuilderSubgraph.
    sub_builder = BuilderSubgraph(builder, group_name="group1")
    # Add a process with input {"K1": 2} and output "E1"
    sub_builder.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"K1": 2},
        output_uid="E1",
    )
    # Compute expected process node uid.
    # For Process, if inputs and output are provided, the uid is constructed as:
    #   f"{workstation_id}_{setup_duration}_{process_duration}_{input_str}__{output.node_id}"
    # where input_str is "material.node_uid_quantity" sorted by material.node_id.
    # For "K1", node_uid is "1", quantity=2; for "E1", node_id is 1.
    expected_uid = "1_2_10_1_2__1"
    # Check that the process node is in the graph.
    assert expected_uid in builder.graph.graph.nodes
    # Check that the edge from input ("K1") to process exists with weight 2.
    input_uid = builder.get_or_add("K1").node_uid  # "1"
    edge_data = builder.graph.graph.get_edge_data(input_uid, expected_uid)
    assert edge_data is not None
    assert edge_data.get("weight") == 2
    # Check that the edge from process to output ("E1") exists with weight 1.
    output_uid = builder.get_or_add("E1").node_uid  # "1"
    edge_data = builder.graph.graph.get_edge_data(expected_uid, output_uid)
    assert edge_data is not None
    assert edge_data.get("weight") == 1


def test_duplicate_process(builder, caplog):
    # Prepare items.
    builder.add_item("K1")
    builder.add_item("E1")
    sub_builder = BuilderSubgraph(builder, group_name="group1")
    caplog.clear()
    # Add the process for the first time.
    sub_builder.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"K1": 2},
        output_uid="E1",
    )
    initial_node_count = len(builder.graph.graph.nodes)
    # Try adding the same process again.
    sub_builder.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"K1": 2},
        output_uid="E1",
    )
    # Node count should remain the same.
    assert len(builder.graph.graph.nodes) == initial_node_count
    # A warning should have been logged.
    assert any("already exists" in record.message for record in caplog.records)


def test_add_edge(builder):
    # Test adding a valid edge directly via MaterialProductFlowGraph.add_edge.
    builder.add_item("K1")
    builder.add_item("K2")
    # Since both items are added, their node_uids are "1" (for both!) according to Item.from_node_id,
    # but for testing, we simulate that they are distinct by adding a suffix manually.
    # Here we adjust the node_uids for testing purposes.
    node1 = builder.get_or_add("K1")
    node2 = builder.get_or_add("K2")
    # Monkey-patch their node_uid properties to simulate distinct uids.
    object.__setattr__(node1, "node_id", 1)
    object.__setattr__(node2, "node_id", 2)
    # Remove existing nodes and re-add with new uids.
    builder.graph.graph.remove_node("1")
    builder.graph.graph.remove_node("1")
    builder.graph.graph.clear()
    builder.material_map["K1"] = node1
    builder.material_map["K2"] = node2
    builder.graph.add_node(node1)
    builder.graph.add_node(node2)
    # Now add a dummy edge.
    builder.graph.add_edge(node1.node_uid, node2.node_uid, weight=3)
    # Check that the edge exists.
    edge_data = builder.graph.graph.get_edge_data("1", "2")
    assert edge_data is not None
    assert edge_data.get("weight") == 3
