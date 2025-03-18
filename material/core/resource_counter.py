from collections import Counter
from dataclasses import dataclass, field
from typing import Self, TypeVar

from material.graph.nodes.graph_nodes import Item, Node, StepProduced

T = TypeVar("T", bound=Node)


class ResourceCounter[T](Counter[T]):
    def _get_entries_sort_value(self, entry: tuple[Node, int]) -> int:
        node, _ = entry
        if isinstance(node, Item):
            return node.node_numerical_id
        return 0

    def print_sorted_resources(self) -> None:
        for key, count in sorted(self.items(), key=lambda x: self._get_entries_sort_value(x)):
            if isinstance(key, Item) and not isinstance(key, StepProduced):
                print(f"{key.node_id}: {count}")


@dataclass
class ResourceCounterBuilder:
    counter: ResourceCounter[Node] = field(default_factory=ResourceCounter)

    def add(self, node: Node, count: int = 1) -> Self:
        self.counter[node] += count
        return self

    def add_items(self, items: list[Item], count: int = 1) -> Self:
        for item in items:
            self.counter[item] += count
        return self

    def build(self):
        return ResourceCounter(self.counter)
