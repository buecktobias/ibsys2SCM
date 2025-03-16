import abc
import logging
from dataclasses import dataclass
from typing import List, Self

import networkx as nx

from material.graph.graph_nodes import Item, Process, NodeAggregate, GraphNode
from material.graph.production_graph_validator import GraphValidator


@dataclass
class BaseGraph(NodeAggregate, abc.ABC):
    """
    Abstract base class for graph aggregates.

    Attributes:
        child_node_aggregates (List[NodeAggregate]): A list of nodes (or node aggregates) contained in the graph.
    """
    child_node_aggregates: List[NodeAggregate]

    def get_nodes(self) -> List[NodeAggregate]:
        """
        Returns all child nodes contained in this aggregate.
        """
        return self.child_node_aggregates

    @abc.abstractmethod
    def add_to_networkx(self, node: NodeAggregate):
        pass

    @abc.abstractmethod
    def add_node(self, node: NodeAggregate) -> None:
        """
        Adds a node to the graph aggregate.
        """
        pass


class MaterialProductFlowGraph(BaseGraph):
    """
    A wrapper around a networkx DiGraph representing a material resource flow.
    This graph must remain a Directed Acyclic Graph (DAG) and adhere to the following rules:
      - After an edge is added, every node must be connected (i.e. not isolated).
      - Only FINAL_PRODUCT nodes (ProductionNodeType.FINAL_PRODUCT) may have no outgoing edges.
      - Allowed edges:
            • Input Edge: from a BOUGHT or PRODUCED node to a PROCESS node.
            • Output Edge: from a PROCESS node to a PRODUCED node with weight 1.
      - Each PROCESS node must have exactly one outgoing edge.
    """

    def __init__(self, graph: nx.DiGraph = None):
        if graph is None:
            graph = nx.DiGraph()
        self.graph: nx.DiGraph = graph
        self.child_node_aggregates: List[NodeAggregate] = []
        self.validator = GraphValidator(self.graph)

    def add_node(self, node: GraphNode) -> None:
        """
        Adds a GraphNode to the graph if it doesn't already exist.
        """
        self.add_to_networkx(node)
        self.child_node_aggregates.append(node)

    def add_to_networkx(self, node: GraphNode):
        node_uid = node.node_uid
        if node_uid in self.graph.nodes:
            logging.warning(f"Node {node_uid} already exists. Skipping addition.")
            return
        self.graph.add_node(node_uid, data=node)

    def get_nodes(self) -> List[GraphNode]:
        """
        Retrieves all nodes stored in the graph.
        """
        return [data["data"] for _, data in self.graph.nodes(data=True)]

    def get_node(self, node_uid: str) -> GraphNode:
        """
        Retrieves a node by its unique identifier.
        """
        return self.graph.nodes[node_uid]["data"]

    def add_edge(self, source_uid: str, target_uid: str, weight: int) -> None:
        """
        Adds an edge between two existing nodes after validating the edge.

        Raises:
            ValueError: If either node does not exist, or if the edge violates the rules,
                        or if the addition results in a cycle or an isolated node.
        """
        if source_uid not in self.graph.nodes or target_uid not in self.graph.nodes:
            raise ValueError("Both source and target must exist in the graph.")

        self.validator.is_adding_edge_valid(source_uid, target_uid, weight)

        self.graph.add_edge(source_uid, target_uid, weight=weight)

        try:
            self.validator.validate()
        except ValueError as e:
            self.graph.remove_edge(source_uid, target_uid)
            raise ValueError(e)

    def __add__(self, other: Self) -> Self:
        """
        Combines two MaterialProductFlowGraphs into one.
        """
        combined = nx.compose_all([self.graph, other.graph])
        return MaterialProductFlowGraph(combined)


class SubGraph(BaseGraph):
    """
    A subgraph that delegates node addition to a parent graph while maintaining its own aggregate.
    """

    def __init__(self, label: str, parent_graph: BaseGraph):
        self.label = label
        self.parent_graph = parent_graph

    def add_to_networkx(self, node: NodeAggregate):
        self.parent_graph.add_to_networkx(node)

    def add_node(self, node: NodeAggregate) -> None:
        """
        Adds a node to both the parent graph and this subgraph's aggregate.
        """
        self.add_to_networkx(node)
        self.child_node_aggregates.append(node)


class GraphBuilder:
    """
    Helper class to build a MaterialProductFlowGraph.

    Provides methods for creating and connecting Item and Process nodes.
    Maintains a mapping of material identifiers to Item nodes.
    """

    def __init__(self):
        self.graph = MaterialProductFlowGraph()
        self.material_map: dict[str, GraphNode] = {}

    def add_item(self, item_id: str) -> None:
        """
        Creates an Item node from item_id and adds it to the graph.

        Args:
            item_id (str): The identifier for the item (must start with 'K' or 'E').
        """
        try:
            item = Item.from_node_id(item_id)
        except Exception as e:
            logging.error(f"Failed to create Item from {item_id}: {e}")
            raise
        self.material_map[item_id] = item
        self.graph.add_node(item)

    def get_or_add(self, node_uid: str) -> GraphNode:
        """
        Retrieves a node from the graph if it exists, otherwise creates a new Item node.
        """
        if node_uid not in self.material_map:
            self.add_item(node_uid)
        return self.material_map[node_uid]

    def build(self):
        """
        Validates the graph and returns the built MaterialProductFlowGraph.
        """
        self.graph.validator.validate()
        return self.graph


class BuilderSubgraph:
    """
    A helper class to add processes to a GraphBuilder's graph within a specific group.
    """

    def __init__(self, graph_builder: GraphBuilder, group_name: str):
        self.graph_builder = graph_builder
        self.subgraph = SubGraph(group_name, graph_builder.graph)

    def convert_input_dict(self, inputs: dict[str, int]) -> dict[GraphNode, int]:
        """
        Converts a dictionary mapping item identifiers to quantities into a dictionary
        mapping Item objects to quantities.
        """
        converted_dict = {}
        for item_id, quantity in inputs.items():
            item = self.graph_builder.get_or_add(item_id)
            converted_dict[item] = quantity
        return converted_dict

    def add_process(
            self,
            workstation_id: int,
            process_duration: int,
            setup_duration: int,
            inputs: dict[str, int] = None,
            output_uid: str = None,
    ) -> None:
        """
        Adds a Process node to the graph with given input and output connections.

        Args:
            workstation_id (int): The workstation identifier.
            process_duration (int): Duration of the process.
            setup_duration (int): Setup duration before the process.
            inputs (dict[str, int], optional): Mapping of input item identifiers to quantities.
            output_uid (str, optional): Identifier of the output item.
        """
        converted_inputs = self.convert_input_dict(inputs) if inputs is not None else {}
        output_item = self.graph_builder.get_or_add(output_uid)

        if not isinstance(output_item, Item):
            raise ValueError(f"Output item {output_uid} must be an Item node.")

        new_process = Process(
            workstation_id=workstation_id,
            process_duration=process_duration,
            setup_duration=setup_duration,
            inputs=converted_inputs,
            output=output_item,
        )

        if new_process.node_uid in self.graph_builder.graph.graph.nodes:
            logging.warning(f"Node {new_process.node_uid} already exists in the graph! Skipping addition.")
            return

        # Directly add the process node with its data.
        self.graph_builder.graph.graph.add_node(new_process.node_uid, data=new_process)
        for material, weight in converted_inputs.items():
            self.graph_builder.graph.graph.add_edge(material.node_uid, new_process.node_uid, weight=weight)

        self.graph_builder.graph.graph.add_edge(new_process.node_uid, output_item.node_uid, weight=1)


if __name__ == '__main__':
    # Example usage:
    # To build a graph, create a GraphBuilder instance, add items and processes,
    # then retrieve the built MaterialProductFlowGraph via get_graph().
    #
    # For example:
    #   builder = GraphBuilder()
    #   builder.add_item("E1")
    #   builder.add_item("K1")
    #   builder.add_process("P1", workstation_id=1, process_duration=10, setup_duration=2,
    #                        input_item_ids=["K1"], output_item_id="E2")
    #   graph = builder.get_graph()
    pass
