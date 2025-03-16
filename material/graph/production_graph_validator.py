import networkx as nx

from material.graph.graph_nodes import GraphNode
from material.graph.production_node_type import ProductionNodeType


class GraphValidator:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def _is_adding_output_edge_valid(self, source_node: GraphNode, target_node: GraphNode, weight: int) -> None:
        if target_node.node_type not in (ProductionNodeType.PRODUCED, ProductionNodeType.FINAL_PRODUCT):
            raise ValueError("Output edge must go to a PRODUCED or Final node.")
        if weight != 1:
            raise ValueError("Output edge must have weight 1.")
        # noinspection PyTypeChecker
        if int(self.graph.out_degree(source_node.node_uid)) != 0:
            raise ValueError(
                "Each node must have exactly one outgoing edge. So for adding to be valid, the out degree must be 0.")

    def is_adding_edge_valid(self, source_uid: str, target_uid: str, weight: int) -> None:
        source_node: GraphNode = self.graph.nodes[source_uid]["data"]
        target_node: GraphNode = self.graph.nodes[target_uid]["data"]
        s_type = source_node.node_type
        t_type = target_node.node_type

        if s_type == ProductionNodeType.PROCESS:
            self._is_adding_output_edge_valid(source_node, target_node, weight)
        elif s_type in (
                ProductionNodeType.BOUGHT, ProductionNodeType.PRODUCED) and t_type != ProductionNodeType.PROCESS:
            raise ValueError("Input edge from a BOUGHT or PRODUCED node must go to a PROCESS node.")
        elif s_type == ProductionNodeType.FINAL_PRODUCT:
            raise ValueError("FINAL_PRODUCT nodes cannot have outgoing edges.")
        else:
            raise ValueError("Unknown ProductionNodeType for source node.")

    def validate_cycle(self) -> None:
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Graph is not a directed acyclic nx_graph (DAG).")

    def validate_connectedness(self) -> None:
        # Every node must be connected (i.e. have degree >= 1)
        for node in self.graph.nodes:
            if self.graph.degree(node) == 0:
                raise ValueError(f"Node {node} is isolated.")

    def validate(self) -> None:
        self.validate_cycle()
        self.validate_connectedness()
