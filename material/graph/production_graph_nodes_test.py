import networkx as nx
import pytest

from material.graph.graph_nodes import Item, Process
from material.graph.production_graph import GraphBuilder, MaterialProductFlowGraph, SubgraphBuilder


def test_build_cycle_raises():
    builder = GraphBuilder()
    builder.add_item("E1")
    builder.add_item("E2")
    # Introduce a cycle manually

    with pytest.raises(Exception):
        builder.nx_graph.add_edge("E1", "E2")
        builder.nx_graph.add_edge("E2", "E1")
        builder.build()


def test_convert_input_dict():
    builder = GraphBuilder()
    builder.add_item("E1")
    builder.add_item("E2")
    subgraph = SubgraphBuilder(builder, "group1")
    inputs = {"E1": 2, "E2": 3}
    converted = subgraph.add_input_dict(inputs)
    for item, count in converted.items():
        assert isinstance(item, Item)
        assert isinstance(count, int)


def test_builder_subgraph_add_process_edges():
    builder = GraphBuilder()
    # Prepare input and output items
    builder.add_item("E1")
    builder.add_item("E2")
    subgraph = SubgraphBuilder(builder, group_name="group1")
    # Add process with an input (E1) and output (E2)
    process = subgraph.add_process(
        workstation_id=1,
        process_duration=10,
        setup_duration=2,
        inputs={"E1": 5},
        output_uid="E2",
    )
    assert process.node_uid is not None, "Process node not added."
    # Verify edge from input item E1 to the process
    input_uid = builder.material_map["E1"].node_uid
    assert builder.nx_graph.nx_graph.has_edge(input_uid, process.node_uid)
    # Verify edge from the process to output item E2 with weight 1
    output_uid = builder.material_map["E2"].node_uid
    assert builder.nx_graph.nx_graph.has_edge(process.node_uid, output_uid)
    assert builder.nx_graph.nx_graph.edges[process.node_uid, output_uid]["weight"] == 1
