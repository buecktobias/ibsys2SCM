import networkx as nx

from scs.core.db.models.graph_models import GraphNode
from scs.graph.db.database_graph_loader import DatabaseGraphLoader


class NxGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edge(self, from_node: GraphNode, to_node: GraphNode, weight: int = 1):
        self.graph.add_node(from_node)
        self.graph.add_node(to_node)
        self.graph.add_edge(from_node.id, to_node.id, weight=weight)

    def build_from_database(self, loader: DatabaseGraphLoader) -> nx.DiGraph:
        for process in loader.load_processes():
            for inp in process.inputs:
                self.add_edge(inp.item, process, weight=inp.quantity)

            self.add_edge(process, process.output)

        return self.graph
