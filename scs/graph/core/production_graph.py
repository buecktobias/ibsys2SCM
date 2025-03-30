import networkx as nx

from scs.core.db.models.graph_models import GraphNode, MaterialGraphORM
from scs.core.db.models.process_models import ProcessORM
from scs.core.db.models.item_models import BoughtItemORM, ProducedItemORM
from scs.graph.core.weighted_edge import WeightedEdge


class ProductionGraph:
    def __init__(
            self,
            nx_di_graph: nx.DiGraph,
            node_id_dict: dict[int, ProcessORM | BoughtItemORM, ProducedItemORM],
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
