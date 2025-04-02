import abc
from dataclasses import dataclass

from scs.core.domain.item_models import GraphNode, Item, ProducedItem
from scs.core.domain.process_domain_model import Process


@dataclass(frozen=True)
class WeightedEdge[T_from: GraphNode, T_to: GraphNode](abc.ABC):
    """
    Represents a weighted edge connecting two nodes in a graph.

    This class is used to encapsulate the connection between two graph nodes. The
    connection includes the "from" node, the "to" node, and the weight of the edge
    representing the cost or distance of the connection. It is designed to be used
    as part of a graph data structure, where edges connect nodes and store
    additional information about the relationship between them.

    Attributes:
        from_node (T_from): The graph node where the edge originates.
        to_node (T_to): The graph node where the edge terminates.
        weight (int): The weight or cost associated with traversing this edge from
            the "from_node" to the "to_node".
    """
    from_node: T_from
    to_node: T_to
    weight: int


@dataclass(frozen=True)
class ProcessInputEdge(WeightedEdge[Item, Process]):
    """Represents an edge in a weighted graph connecting an Item and a Process.

    This class defines a frozen dataclass to model the edge between an Item
    and a Process in a weighted graph. It inherits properties and behavior from
    the base class WeightedEdge, leveraging the frozen attribute of the
    dataclass decorator to ensure immutability.
    Attributes:
    from_node (Item): The graph node where the edge originates.
    to_node (Process): The graph node where the edge terminates.
    weight (int): The weight or cost associated with traversing this edge from
        the "from_node" to the "to_node".
    """
    pass


@dataclass(frozen=True)
class ProcessOutputEdge(WeightedEdge[Process, ProducedItem]):
    """
    Represents an edge in a graph that connects a process node to a produced item node.

    This class is used to define a weighted edge between a process (source) and a
    produced item (destination) in a graph representation. It is immutable and
    inherits from `WeightedEdge` with `Process` as the source type and
    `ProducedItem` as the destination type.

    Attributes:
    from_node (Process): The graph node where the edge originates.
    to_node (Produced): The graph node where the edge terminates.
    weight (int): The weight is 1;
    """
    weight: int = 1

    def __post_init__(self):
        if self.weight != 1:
            raise ValueError("Weight of ProcessOutputEdge must be 1.")
