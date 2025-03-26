import abc
from dataclasses import dataclass

from scs.db.models.graph_node import GraphNode


@dataclass()
class WeightedEdge(abc.ABC):
    from_node: GraphNode
    to_node: GraphNode
    weight: int



class InputEdge