from collections import Counter
from dataclasses import dataclass, field
from typing import Iterator, Self

from material.graph.graph_nodes import Item


@dataclass(frozen=True)
class ResourceCounter:
    items: Counter[Item] = field(default_factory=Counter)

    def __add__(self, other: Self) -> Self:
        return ResourceCounter(self.items + other.items)

    def __sub__(self, other: Self) -> Self:
        result = self.items.copy()
        for key, value in other.items.items():
            result[key] -= value
            if result[key] <= 0:
                del result[key]
        return ResourceCounter(result)

    def __mul__(self, multiplier: int) -> Self:
        new_items = Counter({item: count * multiplier for item, count in self.items.items()})
        return ResourceCounter(new_items)

    def __rmul__(self, multiplier: int) -> Self:
        return self.__mul__(multiplier)

    def __getitem__(self, item: Item) -> int:
        return self.items.get(item, 0)

    def __iter__(self) -> Iterator:
        return iter(self.items)

    def __repr__(self) -> str:
        return f"ResourceCounter({dict(self.items)})"

    def get_entries_sort_value(self, entry: tuple[Item, int]) -> int:
        return entry[0].node_id

    def print_sorted_resources(self) -> None:
        for item, count in sorted(self.items.items(), key=lambda x: self.get_entries_sort_value(x)):
            print(f"{item}: {count}")

    def copy(self) -> Self:
        return ResourceCounter(self.items.copy())

    def update(self, other: Self) -> Self:
        return ResourceCounter(self.items + other.items)
