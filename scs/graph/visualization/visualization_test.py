import matplotlib.pyplot as plt
import networkx as nx

from scs.core.db.config import engine
from scs.graph.db.database_graph_loader import DatabaseGraphLoader
from scs.graph.core.graph_validator import GraphValidator
from scs.graph.core.nx_graph_builder import NxGraphBuilder

if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        loader = DatabaseGraphLoader(session)
        graph = NxGraphBuilder().build_from_database(loader)

    for layer, nodes in enumerate(nx.topological_generations(graph)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer minutes as a node attribute
        for node in nodes:
            graph.nodes[node]["layer"] = layer

    # Compute the multipartite_layout using the "layer" node attribute
    pos = nx.multipartite_layout(graph, subset_key="layer")
    GraphValidator(graph).validate()

    plt.figure(figsize=(40, 40))
    nx.draw_networkx_nodes(graph, pos, node_size=800)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.6)
    nx.draw_networkx_labels(graph, pos, font_size=10)

    plt.axis("off")
    plt.show()
