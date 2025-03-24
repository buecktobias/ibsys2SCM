import networkx as nx

from material.db.models import Item
from material.graph.production_graph.database_graph_loader import DatabaseGraphLoader
from material.graph.production_graph.nx_graph_builder import NxGraphBuilder
from material.graph.visualization.mermaid_visualizations import VisualizationMaterialGraph


class ProductionGraph:
    def __init__(self, loader: DatabaseGraphLoader):
        self.nx: nx.DiGraph = NxGraphBuilder().build_from_database(loader)
        self.material_root = loader.load_material_graph_root()

    def prune_singleton_produced_items(self):
        to_remove = []
        for node in list(self.nx.nodes):
            node_data = self.nx.nodes[node].get("_data")
            # Only consider nodes representing an Item that is produced.
            if isinstance(node_data, Item) and node_data.is_produced():
                in_edges = list(self.nx.in_edges(node, data="weight"))
                out_edges = list(self.nx.out_edges(node, data="weight"))
                # Only prune produced items with exactly one incoming and one outgoing edge, both with weight 1.
                if len(in_edges) == 1 and len(out_edges) == 1:
                    if in_edges[0][2] == 1 and out_edges[0][2] == 1:
                        pred = in_edges[0][0]
                        succ = out_edges[0][1]
                        # Reconnect predecessor to successor.
                        self.nx.add_edge(pred, succ, weight=1)
                        to_remove.append(node)
        self.nx.remove_nodes_from(to_remove)

    def build_visualization_material_graph(self):
        """Build a new visualization tree that mirrors the MaterialGraphORM tree but only
           includes processes that are still present in the pruned NX graph.
        """
        return VisualizationMaterialGraph(self.material_root, self.nx)
