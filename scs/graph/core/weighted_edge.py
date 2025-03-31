import abc
from dataclasses import dataclass

from scs.core.db.models.graph_models import GraphNodeORM


@dataclass()
class WeightedEdge(abc.ABC):
    from_node: GraphNodeORM
    to_node: GraphNodeORM
    weight: int
