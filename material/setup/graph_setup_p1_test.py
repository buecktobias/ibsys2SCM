from material.setup import graph_setup_p1


def test_p1_is_dag():
    assert graph_setup_p1.is_dag(create_graph_p1())
