from graph_setup_p1 import create_graph_p1
from graph_setup_p2 import create_graph_p2
from graph_setup_p3 import create_graph_p3
from material.production_graph import MaterialProductionsGraph



def create_full_production_graph():
    graph_p1 = create_graph_p1()
    graph_p2 = create_graph_p2()
    graph_p3 = create_graph_p3()

    return MaterialProductionsGraph(graph_p1, graph_p2, graph_p3)