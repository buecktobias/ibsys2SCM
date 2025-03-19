import networkx as nx

from material.graph.nodes.graph_nodes import Node
from material.graph.nodes.production_node_type import ProductionNodeType


class GraphValidator:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def _is_adding_output_edge_valid(self, source_node: Node, target_node: Node, weight: int) -> None:
        if target_node.node_type != ProductionNodeType.PRODUCED:
            raise ValueError(f"Output edge must go to a PRODUCED or Final node. {source_node} -> {target_node}")
        if weight != 1:
            raise ValueError(f"Output edge must have weight 1. {source_node} -> {target_node}")
        # noinspection PyTypeChecker
        if int(self.graph.out_degree(source_node.label)) != 0:
            raise ValueError(
                "Each node must have exactly one outgoing edge. So for adding to be valid, the out degree must be 0." +
                f" {source_node} -> {target_node}"

            )

    def _is_adding_input_edge_valid(self, source_node: Node, target_node: Node, weight: int) -> None:
        if source_node.node_type not in (ProductionNodeType.BOUGHT, ProductionNodeType.PRODUCED):
            raise ValueError(f"Input edge must come from a PRODUCED or Final node. {source_node} -> {target_node}")
        if weight <= 0:
            raise ValueError(f"Input edge must have a positive weight. {source_node} -> {target_node}")

    def is_adding_edge_valid(self, source_node: Node, target_node: Node, weight: int) -> None:
        if source_node.node_type == ProductionNodeType.PROCESS:
            self._is_adding_output_edge_valid(source_node, target_node, weight)
        elif target_node.node_type == ProductionNodeType.PROCESS:
            self._is_adding_input_edge_valid(source_node, target_node, weight)
        else:
            raise ValueError(f"Unknown ProductionNodeType"
                             f"for source node: {source_node.node_type}")

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
