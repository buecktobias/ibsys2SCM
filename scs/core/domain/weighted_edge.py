import abc
from dataclasses import dataclass

from scs.core.db.models.graph_models import GraphNode


@dataclass()
class WeightedEdge(abc.ABC):
    from_node: GraphNode
    to_node: GraphNode
    weight: int
