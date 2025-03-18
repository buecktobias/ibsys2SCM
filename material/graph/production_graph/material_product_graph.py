import logging
from typing import Self

import networkx as nx

from material.graph.base_graph import BaseGraph
from material.graph.nodes.graph_nodes import Node
from material.graph.production_graph.production_graph_validator import GraphValidator
from material.graph.sub_graph import SubGraph


class MaterialProductGraph(BaseGraph):
    """
    A wrapper around a networkx DiGraph representing a material resource flow.
    This is a DAG
    """

    def create_subgraph(self, label: str) -> Self:
        return SubGraph(label, self)

    def __init__(self, graph: nx.DiGraph = None):
        super().__init__()
        self.__nx_graph: nx.DiGraph = nx.DiGraph() if graph is None else graph
        self._validator = GraphValidator(self.nx_graph)
        logging.debug("Initialized MaterialProductGraph with _validator.")

    @property
    def nx_graph(self) -> nx.DiGraph:
        return self.__nx_graph

    def add_edge(self, source_node: Node, target_node: Node, weight: int = 1) -> None:
        """
        Adds an edge between two existing nodes after validating the edge.
        """
        if not all(self.has_node(node) for node in (source_node, target_node)):
            logging.error(f"Cannot add edge: either {source_node} or {target_node} does not exist.")
            raise ValueError("Both source and target must exist in the nx_graph.")

        logging.info(f"Attempting to add edge from {source_node} to {target_node} with weight {weight}.")
        self._validator.is_adding_edge_valid(source_node, target_node, weight)

        self.nx_graph.add_edge(source_node, target_node, weight=weight)
        logging.debug(f"Edge added from {source_node} to {target_node} with weight {weight}.")

    def validate(self) -> None:
        self._validator.validate()
