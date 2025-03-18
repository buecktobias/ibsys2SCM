import logging

import networkx as nx

from material.core.resource_counter import ResourceCounter
from material.graph.base_graph import BaseGraph
from material.graph.nodes.graph_nodes import NodeAggregate, Node
from material.graph.nodes.process import Process
from material.graph.production_graph.material_product_graph import MaterialProductGraph


class SubGraph(BaseGraph):
    """
    A subgraph that delegates node addition to a parent nx_graph while maintaining its own aggregate.
    """

    def __init__(self, label: str, parent_graph: MaterialProductGraph):
        super().__init__()
        self.label = label
        self.parent_graph = parent_graph
        self.processes: set[Process] = set()
        self._child_node_aggregates = []

    @property
    def nx_graph(self) -> nx.DiGraph:
        return self.parent_graph.nx_graph

    def add_node(self, node: NodeAggregate) -> None:
        self._child_node_aggregates.append(node)
        if isinstance(node, Node):
            logging.info(f"Adding node {node.node_id} to child aggregates.")
        self.add_to_networkx(node)

    def _add_edges(self, from_resources: ResourceCounter, process: Process) -> None:
        """
        Adds edges to the nx_graph from input resources to the process and from the process to the _output item.
        """
        for item, quantity in from_resources.items():
            if not self.has_node(item):
                logging.info(f"Item {item} not found in subgraph; adding it.")
                self.add_node(item)
            self.parent_graph.add_edge(item, process, weight=quantity)
            logging.debug(f"Added edge from {item} to {process} with weight {quantity}.")
        self.parent_graph.add_edge(process, process.output)

    def add_process(
            self,
            new_process: Process,
    ) -> Process | None:

        if self.has_node(new_process) or new_process in self.processes:
            logging.warning(f"Node {new_process} already exists in the nx_graph! Skipping addition.")
            return None

        self.add_node(new_process.output)
        self.add_node(new_process)
        self._add_edges(new_process.inputs, new_process)

        self.parent_graph.add_edge(new_process, new_process.output)
        self.processes.add(new_process)
        logging.debug(f"Added edge from {new_process} to {new_process.output} with weight 1.")

        return new_process
