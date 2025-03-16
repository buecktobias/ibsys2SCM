import abc
from dataclasses import dataclass
from typing import Self

from material.graph.production_node_type import ProductionNodeType


@dataclass(frozen=True)
class Node(abc.ABC):
    """
    Abstract base class representing a nx_graph node.

    Each node must provide its type and a unique identifier (uid).
    """

    @property
    @abc.abstractmethod
    def node_type(self):
        """
        Returns the production node type of the node.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def node_uid(self):
        """
        Returns the unique identifier for the node.
        """
        raise NotImplementedError


class NodeAggregate(abc.ABC):
    """
    Abstract base class for aggregates of nodes.

    Provides an interface to retrieve a list of nodes.
    """

    @abc.abstractmethod
    def get_nodes(self) -> list[Self]:
        """
        Returns a list of nodes contained in the aggregate.
        """
        pass


class GraphNode(Node, NodeAggregate):
    """
    A concrete implementation of a node that also aggregates itself.

    This class serves as a wrapper to treat single nodes as aggregates.
    """

    @property
    def node_type(self):
        """
        Returns the node type.

        For an Item, returns its underlying production type; for a Process, always returns PROCESS.
        """
        if isinstance(self, Item):
            return self._node_type
        if isinstance(self, Process):
            return ProductionNodeType.PROCESS
        raise ValueError(f"Unknown node type: {self}")

    @property
    def node_uid(self):
        """
        Returns the unique identifier of the node.

        This implementation delegates to the specific implementations in Item or Process.
        """
        if isinstance(self, Item):
            return Item.node_uid.fget(self)  # call the getter of Item.node_uid
        if isinstance(self, Process):
            return Process.node_uid.fget(self)
        raise ValueError(f"Unknown node type: {self}")

    def get_nodes(self) -> list[NodeAggregate]:
        """
        Returns a list containing this node.
        """
        return [self]


@dataclass(frozen=True)
class Item(GraphNode):
    """
    Represents an item node in the nx_graph.

    Attributes:
        node_id (int): The numerical identifier of the item.
        _node_type (ProductionNodeType): The type of the item, either BOUGHT or PRODUCED.
    """
    node_id: int
    _node_type: ProductionNodeType

    @property
    def node_type(self):
        """
        Returns the production node type of the item.
        """
        return self._node_type

    @property
    def node_uid(self):
        """
        Returns the unique identifier for the item as a string.
        """
        return str(self.node_id)

    @staticmethod
    def from_node_id(node_id: str) -> "Item":
        """
        Creates an Item instance from a string node identifier.

        The node_id must start with 'K' or 'E'. If it starts with 'E', the node is
        considered to be PRODUCED; otherwise, it is BOUGHT.

        Args:
            node_id (str): The string identifier of the node.

        Returns:
            Item: An instance of Item.

        Raises:
            ValueError: If the node_id does not start with 'K' or 'E'.
        """
        if node_id[0] not in ["K", "E"]:
            raise ValueError(f"Node id must start with K or E: {node_id}")
        numerical_id = int(node_id[1:])
        return Item(numerical_id, ProductionNodeType.PRODUCED if "E" in node_id else ProductionNodeType.BOUGHT)


@dataclass(frozen=True)
class StepItem(Item):
    """
    Represents a step item in the nx_graph, extending an Item with a step number.

    Attributes:
        step_number (int): The specific step associated with this item.
    """
    step_number: int

    @property
    def node_uid(self):
        """
        Returns a unique identifier for the step item that includes the step number.
        """
        return f"{self.node_id}_{self.step_number}"


@dataclass(frozen=True)
class Process(GraphNode):
    """
    Represents a process node in the nx_graph.

    Attributes:
        workstation_id (int): The identifier for the workstation.
        process_duration (int): The duration of the process.
        setup_duration (int): The setup duration before the process.
        inputs (dict[Item, int], optional): A dictionary mapping input Items to their required quantities.
        output (Item, optional): The output Item of the process.
    """
    workstation_id: int
    process_duration: int
    setup_duration: int
    inputs: dict[Item, int] = None
    output: Item = None

    @property
    def node_type(self):
        """
        Returns the production node type for a process, which is always PROCESS.
        """
        return ProductionNodeType.PROCESS

    @property
    def node_uid(self):
        """
        Generates a unique identifier for the process node based on its parameters.

        The identifier is composed of the workstation_id, setup_duration, process_duration,
        a sorted string representation of its inputs, and the output's node_id (if provided).

        Returns:
            str: The unique identifier for the process node.
        """
        if not self.inputs or not self.output:
            return f"{self.workstation_id}_{self.setup_duration}_{self.process_duration}"
        input_str = "_".join(
            f"{material.node_uid}_{quantity}"
            for material, quantity in sorted(self.inputs.items(), key=lambda x: x[0].node_id)
        )
        return f"{self.workstation_id}_{self.setup_duration}_{self.process_duration}_{input_str}__{self.output.node_id}"
