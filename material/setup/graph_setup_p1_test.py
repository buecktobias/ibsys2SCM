from material.setup import graph_setup_p1


def test_create_graph_p1():
    graph = graph_setup_p1.create_graph_p1()
    assert graph is not None
    assert len(graph.nx_graph.nodes) > 0
    assert len(graph.nx_graph.edges) > 0
