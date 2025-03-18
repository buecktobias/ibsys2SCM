import abc
import logging
from typing import List

import networkx as nx

from material.graph.nodes.graph_nodes import NodeAggregate, Node


class BaseGraph(NodeAggregate, abc.ABC):
    """
    Abstract base class for nx_graph aggregates.

    Attributes:
        child_node_aggregates (List[NodeAggregate]): A list of node aggregates
    """

    def __init__(self):
        self.child_node_aggregates: List[NodeAggregate] = []

    @property
    @abc.abstractmethod
    def nx_graph(self) -> nx.DiGraph:
        raise NotImplementedError

    def get_node_aggregates(self) -> List[NodeAggregate]:
        """
        Returns all child nodes contained in this aggregate.
        """
        return self.child_node_aggregates

    def add_to_networkx(self, node: NodeAggregate):
        if isinstance(node, Node):
            self.nx_graph.add_node(node.node_id, data=node)
            logging.debug(f"Added node {node.node_id} to networkx graph.")
        else:
            logging.info(f"Node {node} is not a Node; skipping addition to networkx graph.")

    def add_node(self, node: NodeAggregate) -> None:
        self.child_node_aggregates.append(node)
        self.add_to_networkx(node)

    def has_node(self, node: Node) -> bool:
        return node.node_id in self.nx_graph.nodes
