import pytest
import networkx as nx
import logging

from material.graph.production_graph import GraphBuilder, BuilderSubgraph, MaterialProductFlowGraph
from material.graph.graph_nodes import Item, Process, StepItem
from material.graph.production_node_type import ProductionNodeType


def test_add_item_duplicate_warning(caplog):
    builder = GraphBuilder()
    caplog.clear()
    builder.add_item("E1")
    initial_count = len(builder.material_graph.nodes)
    builder.add_item("E1")  # Duplicate addition
    assert len(builder.material_graph.nodes) == initial_count
    assert any("already exists" in record.message for record in caplog.records)


def test_build_cycle_raises():
    builder = GraphBuilder()
    builder.add_item("E1")
    builder.add_item("E2")
    # Introduce a cycle manually
    builder.material_graph.add_edge("E1", "E2")
    builder.material_graph.add_edge("E2", "E1")
    with pytest.raises(Exception):
        builder.build()


def test_convert_input_dict():
    builder = GraphBuilder()
    builder.add_item("E1")
    builder.add_item("E2")
    subgraph = builder.create_group_builder("group1")
    inputs = {"E1": 2, "E2": 3}
    converted = subgraph.convert_input_dict(inputs)
    for item, count in converted.items():
        assert isinstance(item, Item)
        assert isinstance(count, int)


def test_builder_subgraph_add_process_edges():
    builder = GraphBuilder()
    # Prepare input and output items
    builder.add_item("E1")
    builder.add_item("E2")
    subgraph = builder.create_group_builder("group1")
    # Add process with an input (E1) and output (E2)
    subgraph.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"E1": 5},
        output="E2"
    )
    # Find the process node added to the material_graph
    process_node_uid = None
    for uid, attr in builder.material_graph.nodes(data=True):
        node_obj = attr.get("data")
        if isinstance(node_obj, Process):
            process_node_uid = uid
            break
    assert process_node_uid is not None, "Process node not added."
    # Verify edge from input item E1 to the process
    input_uid = builder.material_map["E1"].node_uid
    assert builder.material_graph.has_edge(input_uid, process_node_uid)
    # Verify edge from the process to output item E2 with weight 1
    output_uid = builder.material_map["E2"].node_uid
    assert builder.material_graph.has_edge(process_node_uid, output_uid)
    assert builder.material_graph.edges[process_node_uid, output_uid]["weight"] == 1


def test_material_product_flow_graph_add_operator():
    # Create first material_graph with one node.
    g1 = nx.DiGraph()
    g1.add_node("A", data="node_A")
    mpg1 = MaterialProductFlowGraph(g1)
    # Create second material_graph with a different node.
    g2 = nx.DiGraph()
    g2.add_node("B", data="node_B")
    mpg2 = MaterialProductFlowGraph(g2)
    combined = mpg1 + mpg2
    nodes = list(combined.material_graph.nodes)
    assert "A" in nodes
    assert "B" in nodes
