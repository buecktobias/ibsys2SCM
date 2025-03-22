from collections import Counter
from dataclasses import dataclass, field
from typing import Self

from material.initialize_db.graph.nodes.graph_nodes import DomainItem
from material.initialize_db.graph.nodes.mermaid_node import LabeledGraphNode


@dataclass
class ResourceCounterBuilder[T]:
    counter: Counter[T] = field(default_factory=Counter)

    def add(self, node: LabeledGraphNode, count: int = 1) -> Self:
        self.counter[node] += count
        return self

    def add_items(self, items: list[DomainItem], count: int = 1) -> Self:
        for item in items:
            self.counter[item] += count
        return self

    def build(self):
        return self.counter
