import abc
from typing import Self

from material.graph.nodes.production_node_type import ProductionNodeType


class NodeAggregate(abc.ABC):
    """
    Abstract base class for aggregates of nodes.

    Provides an interface to retrieve a list of nodes.
    """

    @abc.abstractmethod
    def get_node_aggregates(self) -> list[Self]:
        """
        Returns a list of nodes contained in the aggregate.
        """
        pass


class Node(NodeAggregate, abc.ABC):
    """
    Abstract base class representing a nx_graph node.
    """

    @property
    @abc.abstractmethod
    def node_type(self) -> ProductionNodeType:
        """
        Returns the production node diagram_type of the node.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def node_id(self) -> str:
        """
        Returns the unique identifier for the node.
        """
        raise NotImplementedError

    def get_node_aggregates(self) -> list[NodeAggregate]:
        """
        Returns a list containing this node.
        """
        return [self]

    def __repr__(self):
        return self.node_id

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.node_id == other.node_id


class Item(Node):
    """
    Represents an item node in the nx_graph.

    Attributes:
        node_numerical_id (int): The numerical identifier of the item.
        _node_type (ProductionNodeType): The diagram_type of the item, either BOUGHT or PRODUCED.
    """

    def __init__(self, node_numerical_id: int, node_type: ProductionNodeType):
        self.node_numerical_id = node_numerical_id
        self._node_type = node_type

    @property
    def node_type(self):
        """
        Returns the production node diagram_type of the item.
        """
        return self._node_type

    @property
    def node_id(self):
        """
        Returns the unique identifier for the item as a string.
        """
        return (
            f"{self.node_type.value}{self.node_numerical_id}"
        )


class Bought(Item):
    """
    Represents a bought item node in the nx_graph.
    """

    def __init__(self, node_numerical_id: int):
        super().__init__(node_numerical_id, ProductionNodeType.BOUGHT)


class Produced(Item):
    """
    Represents a produced item node in the nx_graph.
    """

    def __init__(self, node_numerical_id: int):
        super().__init__(node_numerical_id, ProductionNodeType.PRODUCED)


class StepProduced(Item):
    def __init__(self, parent_produced: Produced, step_number: int):
        super().__init__(parent_produced.node_numerical_id, ProductionNodeType.PRODUCED)
        self.parent_produced = parent_produced
        self.step_number = step_number

    @property
    def node_id(self) -> str:
        return f"{self.parent_produced.node_id}_{self.step_number}"

    @property
    def node_type(self) -> ProductionNodeType:
        return ProductionNodeType.PRODUCED
