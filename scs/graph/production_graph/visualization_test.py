import matplotlib.pyplot as plt
import networkx as nx

from scs.db.config import engine
from scs.graph.production_graph.database_graph_loader import DatabaseGraphLoader
from scs.graph.production_graph.graph_validator import GraphValidator
from scs.graph.production_graph.nx_graph_builder import NxGraphBuilder

if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        loader = DatabaseGraphLoader(session)
        graph = NxGraphBuilder().build_from_database(loader)

    GraphValidator(graph).validate()

    pos = nx.spring_layout(graph, k=1, iterations=200)

    plt.figure(figsize=(20, 20))
    nx.draw_networkx_nodes(graph, pos, node_size=800)
    nx.draw_networkx_edges(graph, pos, width=1.5, alpha=0.7)
    nx.draw_networkx_labels(graph, pos, font_size=10)

    plt.axis("off")
    plt.tight_layout()
    plt.show()
