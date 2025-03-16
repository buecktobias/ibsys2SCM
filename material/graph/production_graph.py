import abc
import logging
from typing import List, Self

import networkx as nx

from material.graph.graph_nodes import Item, Process, NodeAggregate, GraphNode
from material.graph.production_graph_validator import GraphValidator


class BaseGraph(NodeAggregate, abc.ABC):
    """
    Abstract base class for nx_graph aggregates.

    Attributes:
        child_node_aggregates (List[NodeAggregate]): A list of nodes (or node aggregates) contained in the nx_graph.
    """

    def __init__(self):
        self.child_node_aggregates: List[NodeAggregate] = []

    @property
    @abc.abstractmethod
    def nx_graph(self) -> nx.DiGraph:
        raise NotImplementedError

    def get_nodes(self) -> List[NodeAggregate]:
        """
        Returns all child nodes contained in this aggregate.
        """
        return self.child_node_aggregates

    def add_to_networkx(self, node: NodeAggregate):
        if isinstance(node, GraphNode):
            self.nx_graph.add_node(node.node_uid, data=node)

    def add_node(self, node: NodeAggregate) -> None:
        self.child_node_aggregates.append(node)
        self.add_to_networkx(node)

    def has_node(self, node_uid: str) -> bool:
        """
        Checks if a node exists in the nx_graph.
        """
        return node_uid in self.nx_graph.nodes

    def get_node(self, node_uid: str) -> GraphNode:
        """
        Retrieves a node by its unique identifier.
        """
        return self.nx_graph.nodes[node_uid]["data"]

    def add_item(self, item_id: str) -> None:
        """
        Creates an Item node from item_id and adds it to the nx_graph.

        Args:
            item_id (str): The identifier for the item (must start with 'K' or 'E').
        """
        try:
            item = Item.from_node_id(item_id)
        except Exception as e:
            logging.error(f"Failed to create Item from {item_id}: {e}")
            raise
        self.nx_graph.add_node(item)

    def __add__(self, other: Self) -> Self:
        """
        Combines two MaterialProductFlowGraphs into one.
        """
        combined = nx.compose_all([self.nx_graph, other.nx_graph])
        return MaterialProductFlowGraph(combined)


class MaterialProductFlowGraph(BaseGraph):
    """
    A wrapper around a networkx DiGraph representing a material resource flow.
    This nx_graph must remain a Directed Acyclic Graph (DAG) and adhere to the following rules:
      - After an edge is added, every node must be connected (i.e. not isolated).
      - Only FINAL_PRODUCT nodes (ProductionNodeType.FINAL_PRODUCT) may have no outgoing edges.
      - Allowed edges:
            • Input Edge: from a BOUGHT or PRODUCED node to a PROCESS node.
            • Output Edge: from a PROCESS node to a PRODUCED node with weight 1.
      - Each PROCESS node must have exactly one outgoing edge.
    """

    def __init__(self, graph: nx.DiGraph = None):
        super().__init__()
        if graph is None:
            graph = nx.DiGraph()
        self._nx_graph: nx.DiGraph = graph
        self.child_node_aggregates: List[NodeAggregate] = []
        self.validator = GraphValidator(self.nx_graph)

    @property
    def nx_graph(self) -> nx.DiGraph:
        return self._nx_graph

    def get_graph_nodes(self):
        return self.nx_graph.nodes

    @property
    def node_id_map(self) -> dict[str, NodeAggregate]:
        return {node.node_uid: node for node in self.get_graph_nodes()}

    def add_edge(self, source_uid: str, target_uid: str, weight: int = 1) -> None:
        """
        Adds an edge between two existing nodes after validating the edge.

        Raises:
            ValueError: If either node does not exist, or if the edge violates the rules,
                        or if the addition results in a cycle or an isolated node.
        """
        if source_uid not in self.nx_graph.nodes or target_uid not in self.nx_graph.nodes:
            raise ValueError("Both source and target must exist in the nx_graph.")

        self.validator.is_adding_edge_valid(source_uid, target_uid, weight)

        self.nx_graph.add_edge(source_uid, target_uid, weight=weight)

        try:
            self.validator.validate()
        except ValueError as e:
            self.nx_graph.remove_edge(source_uid, target_uid)
            raise ValueError(e)


class SubGraph(BaseGraph):
    """
    A subgraph that delegates node addition to a parent nx_graph while maintaining its own aggregate.
    """

    def __init__(self, label: str, parent_graph: BaseGraph):
        super().__init__()
        self.label = label
        self.parent_graph = parent_graph

    @property
    def nx_graph(self) -> nx.DiGraph:
        return self.parent_graph.nx_graph

    def add_input_dict(self, inputs: dict[str, int]) -> dict[GraphNode, int]:
        """
        Converts a dictionary mapping item identifiers to quantities into a dictionary
        mapping Item objects to quantities.
        """
        converted_dict = {}
        for item_id, quantity in inputs.items():
            if not self.has_node(item_id):
                self.add_node(Item.from_node_id(item_id))
            item = self.get_node(item_id)
            converted_dict[item] = quantity
        return converted_dict

    def add_process(
            self,
            workstation_id: int,
            process_duration: int,
            setup_duration: int,
            inputs: dict[str, int] = None,
            output_uid: str = None,
    ) -> Process | None:
        """
        Adds a Process node to the nx_graph with given input and output connections.

        Args:
            workstation_id (int): The workstation identifier.
            process_duration (int): Duration of the process.
            setup_duration (int): Setup duration before the process.
            inputs (dict[str, int], optional): Mapping of input item identifiers to quantities.
            output_uid (str, optional): Identifier of the output item.
        """
        converted_inputs = self.add_input_dict(inputs) if inputs is not None else {}
        self.add_node(Item.from_node_id(output_uid))
        output_item = self.get_node(output_uid)

        if not isinstance(output_item, Item):
            raise ValueError(f"Output item {output_uid} must be an Item node.")

        new_process = Process(
            workstation_id=workstation_id,
            process_duration=process_duration,
            setup_duration=setup_duration,
            inputs=converted_inputs,
            output=output_item,
        )

        if self.has_node(new_process.node_uid):
            logging.warning(f"Node {new_process.node_uid} already exists in the nx_graph! Skipping addition.")
            return None

        # Directly add the process node with its data.
        self.add_node(new_process)
        for material, weight in converted_inputs.items():
            self.nx_graph.add_edge(material.node_uid, new_process.node_uid, weight=weight)

        self.nx_graph.add_edge(new_process.node_uid, output_item.node_uid, weight=1)

        return new_process


if __name__ == '__main__':
    # Example usage:
    # To build a nx_graph, create a GraphBuilder instance, add items and processes,
    # then retrieve the built MaterialProductFlowGraph via get_graph().
    #
    # For example:
    #   builder = GraphBuilder()
    #   builder.add_item("E1")
    #   builder.add_item("K1")
    #   builder.add_process("P1", workstation_id=1, process_duration=10, setup_duration=2,
    #                        input_item_ids=["K1"], output_item_id="E2")
    #   nx_graph = builder.get_graph()
    pass
