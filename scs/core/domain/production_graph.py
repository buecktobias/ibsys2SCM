import networkx as nx

from scs.core.db.graph.material_graph_orm import MaterialGraphORM
from scs.core.domain.graph.edge_models import WeightedEdge
from scs.core.domain.item_models import BoughtItem, GraphNode, ProducedItem
from scs.core.domain.process_domain_model import Process


class ProductionGraph:
    def __init__(
            self,
            nx_di_graph: nx.DiGraph,
            node_id_dict: dict[int, Process | BoughtItem, ProducedItem],
            root_orm_graph: MaterialGraphORM
    ):
        self._nx: nx.DiGraph = nx_di_graph
        self._node_id_dict = node_id_dict
        self._root_or_graph = root_orm_graph

    def get_node_by_id(self, node_id: int) -> GraphNode:
        return self._node_id_dict[node_id]

    @property
    def nx_graph(self) -> nx.DiGraph:
        return self.nx_graph

    @property
    def node_ids(self):
        return self.nx_graph.nodes

    @property
    def edges(self) -> list[WeightedEdge]:
        return [
                WeightedEdge(
                        from_node=self.get_node_by_id(from_node),
                        to_node=self.get_node_by_id(to_node),
                        weight=weight
                ) for from_node, to_node, weight in
                self.nx_graph.edges(data="weight", default=1)
        ]

    def out_degree(self, node: GraphNode) -> int:
        node_id = node.id
        return len(self.nx_graph.out_degree(node_id))
